from fastapi import Depends, HTTPException, status
from app.auth.auth_user_bearer import get_current_user
from app.schemas.user_schema import UserRead
from app.auth.auth_client_bearer import get_current_client
from app.schemas.client_schema import ClientRead

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

def clients_only(current_client: ClientRead = Depends(get_current_client)):
    if not current_client.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive client."
        )
    return current_client
