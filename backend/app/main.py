from fastapi import FastAPI
from .api.user_router import router as user_router
from .database.init_db import init_db
from .core.exception_handler import register_exception_handlers

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

app.include_router(user_router)
