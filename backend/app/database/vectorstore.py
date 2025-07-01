import redis
from typing import Callable, Any
from langchain_redis import RedisConfig, RedisVectorStore
from app.core.config import settings
from app.core.ollama_client import get_ollama_embeddings
from sqlalchemy.orm import Session
from app.models.chat_question_model import ChatQuestion
from app.models.chat_message_model import ChatMessage
from app.models.chat_session_model import ChatSession
from app.core.constants.sender import SenderEnum
from app.core.constants.feedback import FeedbackEnum

class ChatVectorStore:
    def __init__(self):
        self.redis_client = redis.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            password=settings.REDIS_PASSWORD,
            decode_responses=True
        )
        self.embeddings = get_ollama_embeddings()
    
    def _delete_existing_ids(self, vector_store, ids: list[str]):
        if ids:
            vector_store.delete(ids=ids)
    
    def _get_schema_for_index(self, index_name: str) -> list[dict]:
        if index_name == "chatbot_questions_index":
            return [
                {"name": "id", "type": "tag"},
                {"name": "question", "type": "text"},
                {"name": "subject", "type": "tag"},
                {"name": "type", "type": "tag"},
            ]
        elif index_name == "chatbot_external_user_history_index":
            return [
                {"name": "id", "type": "tag"},
                {"name": "external_user_id", "type": "tag"},
                {"name": "type", "type": "tag"},
            ]
        else:
            raise ValueError(f"❌ Esquema de metadados não definido para o índice '{index_name}'")
    
    def get_vectorstore_config(self, index_name: str, metadata_schema: list[dict]) -> RedisConfig:
        return RedisConfig(
            index_name=index_name,
            redis_url=f"redis://:{settings.REDIS_PASSWORD}@{settings.REDIS_HOST}:{settings.REDIS_PORT}",
            metadata_schema=metadata_schema,
            recreate_index=False,
            id_field="id"
        )

    def get_vectorstore(self, index_name: str) -> RedisVectorStore:
        schema = self._get_schema_for_index(index_name)
        config = self.get_vectorstore_config(index_name, schema)
        return RedisVectorStore(self.embeddings, config=config)
    
    def _prepare_texts_and_metadatas(
        self,
        items: list[Any],
        extractor: Callable[[Any], tuple[str, dict]]
    ) -> tuple[list[str], list[dict]]:
        texts, metadatas = [], []
        for item in items:
            text, metadata = extractor(item)
            texts.append(text)
            metadatas.append(metadata)
        return texts, metadatas

    def _filter_existing_ids(self, vector_store, ids: list[str]) -> set[str]:
        existing_docs = vector_store.get_by_ids(ids)
        existing_ids = {doc.metadata.get("id") for doc in existing_docs if doc.metadata.get("id")}
        return existing_ids

    def build_vectorstore_from_questions(self, db: Session):
        index_name = "chatbot_questions_index"

        vector_store = self.get_vectorstore(index_name)
        questions = db.query(ChatQuestion).all()

        texts, metadatas, ids = [], [], []

        for q in questions:
            q_id = str(q.id)
            text = q.question + "\n" + "\n".join([a.answer for a in q.answers])
            metadata = {
                "id": q_id,
                "question": q.question,
                "subject": q.subject or "",
                "type": "document"
            }
            texts.append(text)
            metadatas.append(metadata)
            ids.append(q_id)

        self._delete_existing_ids(vector_store, ids)

        vector_store.add_texts(texts=texts, metadatas=metadatas, ids=ids)

        print(f"✅ {len(texts)} questões indexadas no Redis sem duplicação.")

    def build_vectorstore_from_external_user_history(self, db: Session, external_user_id: int):
        index_name = "chatbot_external_user_history_index"
        
        vector_store = self.get_vectorstore(index_name)
        messages = db.query(ChatMessage).join(ChatSession).filter(
            ChatSession.external_user_id == external_user_id
        ).order_by(ChatMessage.session_id, ChatMessage.created_at).all()

        if not messages:
            print(f"⚠️ Nenhuma mensagem encontrada para external_user_id={external_user_id}")
            return

        pairs = []
        previous = None

        for msg in messages:
            if msg.sender == SenderEnum.USER:
                previous = msg
            elif msg.sender == SenderEnum.BOT and previous:
                if msg.feedback != FeedbackEnum.NEGATIVE:
                    pairs.append((previous, msg))
                previous = None

        if not pairs:
            print(f"⚠️ Nenhum par usuário + bot encontrado para external_user_id={external_user_id}")
            return

        ids = [f"external_user_id_{external_user_id}_msg_{user_msg.id}" for user_msg, _ in pairs]
        existing_ids = self._filter_existing_ids(vector_store, ids)

        new_texts, new_metadatas, new_ids = [], [], []
        for (user_msg, bot_msg), msg_id in zip(pairs, ids):
            if msg_id in existing_ids:
                continue

            text = f"Usuário: {user_msg.message}\nBot: {bot_msg.message}"
            metadata = {
                "id": msg_id,
                "external_user_id": str(external_user_id),
                "type": "external_user_bot_pair"
            }
            new_texts.append(text)
            new_metadatas.append(metadata)
            new_ids.append(msg_id)

        if new_texts:
            vector_store.add_texts(texts=new_texts, metadatas=new_metadatas, ids=new_ids)
            print(f"✅ {len(new_texts)} novas interações indexadas para o usuário {external_user_id}.")
        else:
            print(f"ℹ️ Nenhuma nova interação para indexar para o usuário {external_user_id}.")
