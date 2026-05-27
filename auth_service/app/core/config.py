from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    postgres_user: str = "bookish_user"
    postgres_password: str = "bookish_password"
    postgres_db: str = "bookish_db"
    postgres_host: str = "localhost"
    postgres_port: int = 5433

    jwt_secret_key: str = "super-secret-key-change-later"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60

    @property
    def database_url(self) -> str:
        return (
            f"postgresql://{self.postgres_user}:"
            f"{self.postgres_password}@{self.postgres_host}:"
            f"{self.postgres_port}/{self.postgres_db}"
        )

    class Config:
        env_file = ".env"


settings = Settings()