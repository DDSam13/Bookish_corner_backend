from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    auth_service_url: str = "http://localhost:8001"
    library_service_url: str = "http://localhost:8002"
    progress_service_url: str = "http://localhost:8005"
    tracker_service_url: str = "http://localhost:8006"
    metadata_service_url: str = "http://localhost:8003"
    recommendation_service_url: str = "http://localhost:8004"

    jwt_secret_key: str = "super-secret-key-change-later"
    jwt_algorithm: str = "HS256"

    class Config:
        env_file = ".env"


settings = Settings()