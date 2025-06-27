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
from app.core.constants.feedback import FeedbackEnum

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
        user_message = self.repository.create(self.db, {
            "session_id": session_id,
            "sender": SenderEnum(1),  # Usuário
            "message": message.message,
            "external_user_id": message.external_user_id
        })

        self.vector_store.build_vectorstore_from_external_user_history(self.db, message.external_user_id)

        bot_response = self.generate_answer_with_rag(user_message.message, external_user_id=message.external_user_id)

        bot_message = self.repository.create(self.db, {
            "session_id": session_id,
            "sender": SenderEnum(2),  # Bot
            "message": bot_response,
            "external_user_id": message.external_user_id
        })

        return {
            "bot_message": ChatMessageRead.from_orm(bot_message),
        }

    def generate_answer_with_rag(self, user_message: str, external_user_id: int = None) -> str:
        try:
            print(f"🔍 Gerando resposta via RAG...")

            questions_index = self.vector_store.get_vectorstore("chatbot_questions_index")
            question_results = questions_index.similarity_search(user_message, k=2)

            history_index = self.vector_store.get_vectorstore("chatbot_external_user_history_index")
            where_clause = {"external_user_id": str(external_user_id)} if external_user_id else None
            history_results = history_index.similarity_search(user_message, k=2, where=where_clause)

            all_results = question_results + history_results

            if not all_results:
                print("⚠️ Nenhum resultado encontrado em nenhum dos índices.")
                return "Desculpe, não encontrei uma resposta para isso."

            context = "\n\n".join([doc.page_content for doc in all_results])

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

            llm = get_ollama_llm()
            response = llm.invoke(formatted_prompt)

            return str(response.content) if hasattr(response, "content") else str(response)

        except Exception as e:
            print(f"❌ Erro ao gerar resposta com RAG: {e}")
            return "Ocorreu um erro ao tentar gerar uma resposta."
        
    def update_message_feedback(self, message_id: int, feedback: FeedbackEnum):
        try:
            updated = self.repository.update_feedback(self.db, message_id, feedback.feedback)
            if not updated:
                raise HTTPException(status_code=404, detail="Mensagem não encontrada")
            return ChatMessageRead.from_orm(updated)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
