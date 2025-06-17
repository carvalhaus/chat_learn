from ..session import SessionLocal
from app.repositories.chat_question_repository import ChatQuestionRepository
from app.repositories.chat_answer_repository import ChatAnswerRepository

def seed_questions_and_answers():
    question_repository = ChatQuestionRepository()
    answer_repository = ChatAnswerRepository()
    db = SessionLocal()

    existing_questions = question_repository.list_all(db)

    if existing_questions:
        print("⚠️ Perguntas já existem. Seed ignorado.")
        db.close()
        return

    data = [
        {
            "question": "Quais são os horários de atendimento?",
            "answer": "Nosso atendimento é de segunda a sexta, das 9h às 18h."
        },
        {
            "question": "Onde vocês estão localizados?",
            "answer": "Estamos localizados na Rua Exemplo, 123, São Paulo - SP."
        },
        {
            "question": "Como posso entrar em contato com o suporte?",
            "answer": "Você pode entrar em contato através do e-mail suporte@exemplo.com."
        },
        {
            "question": "Vocês oferecem reembolso?",
            "answer": "Sim, oferecemos reembolso em até 7 dias após a compra, conforme o Código de Defesa do Consumidor."
        },
        {
            "question": "Quais serviços vocês oferecem?",
            "answer": "Oferecemos desenvolvimento web, aplicativos mobile e soluções em nuvem."
        },
        {
            "question": "Como funciona o processo de contratação?",
            "answer": "Basta entrar em contato, entender suas necessidades e enviaremos uma proposta personalizada."
        },
        {
            "question": "O atendimento é online ou presencial?",
            "answer": "Atendemos tanto online quanto presencialmente, conforme sua preferência."
        },
    ]

    try:
        for item in data:
            created_question = question_repository.create(db, {"question": item["question"]})

            answer_repository.create(db, {
                "question_id": created_question.id,
                "answer": item["answer"]
            })

        db.commit()

    except Exception as e:
        db.rollback()
        print(f"Erro no seed: {e}")
    finally:
        db.close()
    
    print("✅ Seed de perguntas e respostas criado com sucesso.")