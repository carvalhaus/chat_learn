from app.schemas.user_schema import UserCreate
from app.services.user_service import UserService

def seed_users():
    user_service = UserService()
    db_users = user_service.list_users()
    
    if db_users:
        print("⚠️ Users already exist. Seed ignored.")
        return

    users = [
        {
            "name": "Admin",
            "email": "admin@example.com",
            "cpf": "12345678901",
            "password": "admin123",
            "gender": 1,
            "phone": "51999999999",
            "birth_date": "1990-01-01",
            "perfil": 1
        },
        {
            "name": "Usuário Teste",
            "email": "user@example.com",
            "cpf": "98765432100",
            "password": "user123",
            "gender": 2,
            "phone": "51988888888",
            "birth_date": "1992-05-15",
            "perfil": 2
        },
    ]

    for u in users:
        user_create = UserCreate(**u)
        user_service.create_user(user_create)

    print("✅ User seeding successfully completed!")