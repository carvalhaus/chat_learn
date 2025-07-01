
from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.auth.auth_client_handler import verify_client_token

security = HTTPBearer()

def get_current_client(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    return verify_client_token(token)
