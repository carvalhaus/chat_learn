from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from app.auth.auth_handler import verify_password, create_access_token
from app.schemas.token_schema import Token
from app.services.user_service import UserService
from datetime import timedelta

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user_service = UserService()

    db_user = user_service.get_by_email(form_data.username)

    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )

    if not verify_password(form_data.password, db_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )
    
    token_data = {
        "sub": str(db_user.id),
        "perfil": db_user.perfil
    }

    access_token = create_access_token(
        token_data,
        expires_delta=timedelta(minutes=60 * 24)
    )

    return {"access_token": access_token, "token_type": "bearer"}
