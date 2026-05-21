from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from ..core.security import create_access_token, hash_password, verify_password
from ..repositories.user_repository import UserRepository
from ..schemas.auth import TokenResponse, UserLogin, UserRegister


class AuthService:
    def __init__(self, db: Session):
        self.user_repository = UserRepository(db)

    def register(self, data: UserRegister):
        existing_user = self.user_repository.get_by_email(data.email)

        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Пользователь с таким email уже существует",
            )

        user = self.user_repository.create(
            email=data.email,
            password_hash=hash_password(data.password),
        )

        access_token = create_access_token(str(user.id))

        return TokenResponse(
            access_token=access_token,
            user=user,
        )

    def login(self, data: UserLogin):
        user = self.user_repository.get_by_email(data.email)

        if not user or not verify_password(data.password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Неверный email или пароль",
            )

        access_token = create_access_token(str(user.id))

        return TokenResponse(
            access_token=access_token,
            user=user,
        )

    def get_current_user(self, user_id: str):
        user = self.user_repository.get_by_id(user_id)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Пользователь не найден",
            )

        return user