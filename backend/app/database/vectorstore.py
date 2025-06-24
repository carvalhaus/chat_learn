from langchain_redis import RedisConfig, RedisVectorStore
from app.core.config import settings
from app.core.ollama_client import get_ollama_embeddings
from sqlalchemy.orm import Session
from app.models.chat_question_model import ChatQuestion
import redis

class ChatVectorStore:
    def __init__(self):
        embeddings = get_ollama_embeddings()
        config = RedisConfig(
            index_name="chatbot_index",
            redis_url=f"redis://:{settings.REDIS_PASSWORD}@{settings.REDIS_HOST}:{settings.REDIS_PORT}",
            metadata_schema=[
                {"name": "id", "type": "tag"},
                {"name": "question", "type": "text"},
                {"name": "subject", "type": "tag"},
                {"name": "type", "type": "tag"},

            ],
        )
        self.vector_store = RedisVectorStore(embeddings, config=config)
        self.redis_client = redis.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            password=settings.REDIS_PASSWORD,
            decode_responses=True
        )

    def drop_index(self):
        try:
            self.redis_client.execute_command("FT.DROPINDEX", "chatbot_index", "DD")
            print("Índice Redis removido com sucesso.")
        except Exception as e:
            print(f"Erro ao remover índice (talvez não exista): {e}")

    def build_vectorstore_from_questions_db(self, db: Session):
        # self.drop_index()

        questions = db.query(ChatQuestion).all()
        ids_to_delete = [str(q.id) for q in questions]
        if ids_to_delete:
            self.vector_store.delete(ids=ids_to_delete)

        texts = []
        metadatas = []

        for q in questions:
            combined = q.question + "\n" + "\n".join([a.answer for a in q.answers])
            texts.append(combined)
            metadatas.append({
                "id": str(q.id),
                "question": q.question,
                "subject": q.subject or "",
                "type": "document"
            })

        self.vector_store.add_texts(texts=texts, metadatas=metadatas)
