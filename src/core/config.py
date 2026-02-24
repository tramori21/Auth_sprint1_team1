from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    project_name: str = Field('auth_service', env='PROJECT_NAME')

    user: str = Field(..., env='POSTGRES_USER')
    password: str = Field(..., env='POSTGRES_PASSWORD')
    host: str = Field(..., env='POSTGRES_HOST')
    port: int = Field(..., env='POSTGRES_PORT')
    db: str = Field(..., env='POSTGRES_DB')

    redis_host: str = Field(..., env='REDIS_HOST')
    redis_port: int = Field(..., env='REDIS_PORT')
    redis_db: int = Field(0, env='REDIS_DB')

    jwt_secret: str = Field(..., env='JWT_SECRET')
    jwt_algorithm: str = Field('HS256', env='JWT_ALGORITHM')
    access_token_expire_minutes: int = Field(
        15, env='ACCESS_TOKEN_EXPIRE_MINUTES')
    refresh_token_expire_days: int = Field(30, env='REFRESH_TOKEN_EXPIRE_DAYS')

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


settings = Settings()
