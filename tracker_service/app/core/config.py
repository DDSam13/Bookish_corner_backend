from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    postgres_user: str = "bookish_user"
    postgres_password: str = "bookish_password"
    postgres_db: str = "bookish_db"
    postgres_host: str = "localhost"
    postgres_port: int = 5432

    @property
    def database_url(self):
        return (
            f"postgresql://{self.postgres_user}:"
            f"{self.postgres_password}@"
            f"{self.postgres_host}:"
            f"{self.postgres_port}/"
            f"{self.postgres_db}"
        )

    class Config:
        env_file = ".env"


settings = Settings()