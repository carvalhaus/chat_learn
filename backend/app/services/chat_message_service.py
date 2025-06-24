from typing import List, Optional
from app.database.session import SessionLocal
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.chat_message_model import ChatMessage
from app.repositories.chat_message_repository import ChatMessageRepository
from app.schemas.chat_message_schema import ChatMessageCreate, ChatMessageRead
from app.repositories.chat_session_repository import ChatSessionRepository
from app.repositories.chat_question_repository import ChatQuestionRepository
from app.core.constants.sender import SenderEnum
from app.core.ollama_client import get_ollama_llm
from app.database.vectorstore import ChatVectorStore
from langchain_core.prompts import ChatPromptTemplate

class ChatMessageService:
    def __init__(self):
        self.db: Session = SessionLocal()
        self.repository = ChatMessageRepository()
        self.session_repository = ChatSessionRepository()
        self.chat_question_repository = ChatQuestionRepository()
        self.vector_store = ChatVectorStore()

    def create_message(self, message_create: ChatMessageCreate) -> ChatMessageRead:
        try:
            session = self.session_repository.get_by_id(self.db, message_create.session_id)
            if not session:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Session with ID {message_create.session_id} not found."
                )

            message = self.repository.create(self.db, message_create.dict())
            return ChatMessageRead.from_orm(message)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Failed to create message: {str(e)}"
            )

    def get_message(self, message_id: int) -> Optional[ChatMessageRead]:
        message = self.repository.get_by_id(self.db, message_id)
        if not message:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Message not found"
            )
        return ChatMessageRead.from_orm(message)

    def list_messages(self) -> List[ChatMessageRead]:
        messages = self.repository.list_all(self.db)
        return [ChatMessageRead.from_orm(m) for m in messages]

    def delete_message(self, message_id: int) -> bool:
        deleted = self.repository.delete(self.db, message_id)
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Message not found"
            )
        return True
    
    def process_message(self, session_id: int, message: ChatMessageCreate):
        # 1. Salva a mensagem do usuário
        user_message = self.repository.create(self.db, {
            "session_id": session_id,
            "sender": SenderEnum(1),  # Usuário
            "message": message.message,
            "external_user_id": message.external_user_id
        })

        # 2. Gera a resposta usando RAG com Ollama
        bot_response = self.generate_answer_with_rag(user_message.message)

        # 3. Salva a resposta do bot
        bot_message = self.repository.create(self.db, {
            "session_id": session_id,
            "sender": SenderEnum(2),  # Bot
            "message": bot_response,
            "external_user_id": message.external_user_id
        })

        # 4. Retorna a resposta do bot
        return {
            "bot_message": ChatMessageRead.from_orm(bot_message),
        }

    def generate_answer_with_rag(self, user_message: str):
        # 1. Busca os documentos mais relevantes no vector store
        results = self.vector_store.vector_store.similarity_search(user_message, k=3)

        if not results:
            return "Desculpe, não encontrei uma resposta para isso."

        # 2. Monta o contexto a partir dos documentos encontrados
        context = "\n\n".join([doc.page_content for doc in results])

        template = """Você é um assistente que responde com base nas informações abaixo.
        Contexto:
        {context}

        Pergunta:
        {question}

        Resposta:
        """

        prompt_template = ChatPromptTemplate.from_template(template)

        formatted_prompt = prompt_template.format_messages(
            context=context,
            question=user_message
        )

        ollama_llm = get_ollama_llm()
        response = ollama_llm.invoke(formatted_prompt)

        return response
