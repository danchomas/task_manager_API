from authx import AuthX, AuthXConfig

config = AuthXConfig(
    JWT_SECRET_KEY="your_secret_key",
    JWT_ACCESS_COOKIE_NAME="my_access_token",
    JWT_TOKEN_LOCATION=["cookies"],
    JWT_HEADER_NAME="Authorization",
    JWT_HEADER_TYPE="Bearer"
)

security = AuthX(config=config)
