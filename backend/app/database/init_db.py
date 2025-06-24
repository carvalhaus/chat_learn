from sqlalchemy import inspect
from .session import engine
from .base import Base
from .seeders.user_seeder import seed_users
from .seeders.questions_answers_seeder import seed_questions_and_answers
from app.database.session import SessionLocal
from app.database.vectorstore import ChatVectorStore

def create_tables():
    inspector = inspect(engine)
    existing_tables = inspector.get_table_names()

    Base.metadata.create_all(bind=engine)

    for table in Base.metadata.tables.keys():
        if table in existing_tables:
            print(f"⚠️ Table '{table}' already exist.")
        else:
            print(f"✅ Table '{table}' created successfully")
            
def load_vectorstore():
    db = SessionLocal()
    try:
        vector_store = ChatVectorStore()
        print("🚀 Iniciando carregamento do Vectorstore Redis...")
        vector_store.build_vectorstore_from_questions_db(db)
        print("✅ Vectorstore Redis carregado com sucesso!")
    except Exception as e:
        print(f"❌ Erro ao carregar Vectorstore: {e}")
    finally:
        db.close()


def init_db():
    create_tables()
    seed_users()
    seed_questions_and_answers()
    load_vectorstore()
