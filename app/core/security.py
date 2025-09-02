from authx import AuthX, AuthXConfig

config = AuthXConfig(
    JWT_SECRET_KEY="your_secret_key",
    JWT_ACCESS_COOKIE_NAME="access_token",
    JWT_REFRESH_COOKIE_NAME="refresh_token",
    JWT_TOKEN_LOCATION=["cookies"],
    JWT_ACCESS_TOKEN_EXPIRES=3000,
    JWT_REFRESH_TOKEN_EXPIRES=30,
    JWT_HEADER_NAME="Authorization",
    JWT_HEADER_TYPE="Bearer",
    JWT_COOKIE_CSRF_PROTECT=False,
)

security = AuthX(config=config)
