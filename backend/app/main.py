from fastapi import FastAPI, Response
from .routers.user_router import router as user_router
from .routers.chat_question_router import router as chat_question_router
from .routers.chat_answer_router import router as chat_answer_router
from .routers.chat_router import router as chat_router
from .routers.client_router import router as client_router
from .auth import auth_router
from .database.init_db import init_db
from .core.exception_handler import register_exception_handlers
from app.core.ollama_client import check_ollama_connection

app = FastAPI(
    title="Chatbot API",
    description="API para gerenciamento do chatbot",
    version="1.0.0",
    root_path="/api"
)

register_exception_handlers(app)

@app.on_event("startup")
def startup_event():
    init_db()
    check_ollama_connection()

app.include_router(user_router)
app.include_router(chat_question_router)
app.include_router(chat_answer_router)
app.include_router(chat_router)
app.include_router(client_router)
app.include_router(auth_router.router)

@app.get("/", tags=["Home"])
def start_server():
    return Response("Server is running.")
