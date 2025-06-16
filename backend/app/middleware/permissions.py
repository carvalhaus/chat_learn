from fastapi import Depends, HTTPException, status
from app.auth.auth_bearer import get_current_user
from app.schemas.user_schema import UserRead


def admin_only(current_user: UserRead = Depends(get_current_user)):
    if current_user.perfil != 1:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to perform this action.",
        )
    return current_user

def user_only(current_user: UserRead = Depends(get_current_user)):
    if current_user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated.",
        )
    return current_user
