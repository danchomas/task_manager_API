from jose import jwt, JWTError


SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"

class Auth:
    def __init__(self, secret_key, algorithm):
        self.secret_key = secret_key
        self.algorithm = algorithm

    def create_access_token(self, data: dict):
        return jwt.encode(data, self.secret_key, algorithm=self.algorithm)

    def verify_token(self, token: str):
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except JWTError:
            return None

auth = Auth(SECRET_KEY, ALGORITHM)
