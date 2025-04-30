import os
import httpx
from fastapi import HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

security = HTTPBearer()

# Get the Auth service URL from environment variable
USER_AUTH_SERVICE_URL = os.getenv("USER_AUTH_SERVICE_URL", "http://localhost:8000")

def verify_jwt_token(credentials: HTTPAuthorizationCredentials = Security(security)):
    token = credentials.credentials
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = httpx.get(f"{USER_AUTH_SERVICE_URL}/verify-token", headers=headers)
        response.raise_for_status()
        return response.json()
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail="Invalid or expired token")
    except httpx.RequestError:
        raise HTTPException(status_code=503, detail="Auth service unavailable")
