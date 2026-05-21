from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    postgres_user: str = "bookish_user"
    postgres_password: str = "bookish_password"
    postgres_db: str = "bookish_db"
    postgres_host: str = "localhost"
    postgres_port: int = 5432

    api_gateway_url: str = "http://localhost:8000"

    gigachat_auth_key: str = ""
    gigachat_scope: str = "GIGACHAT_API_PERS"
    gigachat_model: str = "GigaChat"
    gigachat_oauth_url: str = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"
    gigachat_chat_url: str = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"

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