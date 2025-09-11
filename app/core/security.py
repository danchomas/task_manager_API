from jose import jwt, JWTError
from fastapi import HTTPException, Security
from fastapi.security import APIKeyHeader


SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
api_key_header = APIKeyHeader(name="Authorization", auto_error=False)

class Auth:
    def __init__(self, secret_key, algorithm):
        self.secret_key = secret_key
        self.algorithm = algorithm

    def create_access_token(self, data: dict):
        return jwt.encode(data, self.secret_key, algorithm=self.algorithm)

    def verify_token(self, api_key: str = Security(api_key_header)):
        if not api_key:
            raise HTTPException(status_code=403, detail="сould not validate credentials")
        try:
            payload = jwt.decode(api_key, self.secret_key, algorithms=[self.algorithm])
            return payload
        except JWTError:
            raise HTTPException(status_code=401, detail="invalid token")


auth = Auth(SECRET_KEY, ALGORITHM)
