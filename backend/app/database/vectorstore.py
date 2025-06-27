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
            recreate_index=True
        )

    def get_vectorstore(self, index_name: str) -> RedisVectorStore:
        schema = self._get_schema_for_index(index_name)
        config = self.get_vectorstore_config(index_name, schema)
        return RedisVectorStore(self.embeddings, config=config)

    def drop_index(self, index_name: str):
        try:
            self.redis_client.execute_command("FT.DROPINDEX", index_name, "DD")
            print(f"Índice Redis '{index_name}' removido com sucesso.")
        except Exception as e:
            print(f"Erro ao remover índice '{index_name}' (talvez não exista): {e}")
    
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

    def build_vectorstore_from_questions(self, db: Session):
        index_name = "chatbot_questions_index"
        self.drop_index(index_name)

        vector_store = self.get_vectorstore(index_name)
        questions = db.query(ChatQuestion).all()
    
        def extractor(q: ChatQuestion):
            text = q.question + "\n" + "\n".join([a.answer for a in q.answers])
            metadata = {
                "id": str(q.id),
                "question": q.question,
                "subject": q.subject or "",
                "type": "document"
            }
            return text, metadata

        texts, metadatas = self._prepare_texts_and_metadatas(questions, extractor)
        vector_store.add_texts(texts=texts, metadatas=metadatas)

    def build_vectorstore_from_external_user_history(self, db: Session, external_user_id: int):
        index_name = "chatbot_external_user_history_index"
        self.drop_index(index_name)
        
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
                pairs.append((previous, msg))
                previous = None

        if not pairs:
            print(f"⚠️ Nenhum par usuário + bot encontrado para external_user_id={external_user_id}")
            return

        texts = []
        metadatas = []

        for user_msg, bot_msg in pairs:
            text = f"Usuário: {user_msg.message}\nBot: {bot_msg.message}"
            metadata = {
                "id": f"external_user_id_{external_user_id}_msg_{user_msg.id}",
                "external_user_id": str(external_user_id),
                "type": "external_user_bot_pair"
            }
            texts.append(text)
            metadatas.append(metadata)

        print(f"📥 Indexando {len(texts)} pares de interação para o usuário {external_user_id}...")
        vector_store.add_texts(texts=texts, metadatas=metadatas)
        print("✅ Embeddings atualizados com sucesso no índice global.")
