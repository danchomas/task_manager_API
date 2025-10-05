import jwt
from fastapi import HTTPException, Security
from fastapi.security import APIKeyHeader


SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"

api_key_header = APIKeyHeader(name="Authorization", auto_error=False)

class Auth:
    def __init__(self, secret_key: str, algorithm: str):
        self.secret_key = secret_key
        self.algorithm = algorithm

    def create_access_token(self, data: dict):
        return jwt.encode(data, self.secret_key, algorithm=self.algorithm)

    def verify_token(self, api_key: str = Security(api_key_header)):
        if not api_key:
            raise HTTPException(status_code=403, detail="Could not validate credentials")
        try:
            # Убираем "Bearer " из заголовка, если есть
            if api_key.startswith("Bearer "):
                api_key = api_key[7:]
            payload = jwt.decode(api_key, self.secret_key, algorithms=[self.algorithm])
            return payload
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail="Invalid token")


auth = Auth(SECRET_KEY, ALGORITHM)