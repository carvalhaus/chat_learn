from sqlalchemy import inspect
from .session import engine
from .base import Base
from .seeders.user_seeder import seed_users
from .seeders.questions_answers_seeder import seed_questions_and_answers

def create_tables():
    inspector = inspect(engine)
    existing_tables = inspector.get_table_names()

    Base.metadata.create_all(bind=engine)

    for table in Base.metadata.tables.keys():
        if table in existing_tables:
            print(f"⚠️ Table '{table}' already exist.")
        else:
            print(f"✅ Table '{table}' created successfully")

def init_db():
    create_tables()
    seed_users()
    seed_questions_and_answers()