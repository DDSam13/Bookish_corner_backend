from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from ..core.security import (
    create_access_token,
    create_refresh_token,
    hash_password,
    hash_token,
    verify_password,
    verify_token,
)
from ..repositories.token_repository import TokenRepository
from ..repositories.user_repository import UserRepository
from ..schemas.auth import TokenResponse, UserLogin, UserRegister


class AuthService:
    def __init__(self, db: Session):
        self.user_repository = UserRepository(db)
        self.token_repository = TokenRepository(db)

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

        refresh_token = create_refresh_token()

        self.token_repository.create_refresh_token(
            user_id=user.id,
            token_hash=hash_token(refresh_token),
        )

        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
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

        refresh_token = create_refresh_token()

        self.token_repository.create_refresh_token(
            user_id=user.id,
            token_hash=hash_token(refresh_token),
        )

        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
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

    def refresh(self, refresh_token: str):
        users = self.user_repository.get_all_active()

        for user in users:
            active_tokens = self.token_repository.get_active_tokens_by_user(user.id)

            for token_record in active_tokens:
                if verify_token(refresh_token, token_record.token_hash):
                    new_access_token = create_access_token(str(user.id))
                    new_refresh_token = create_refresh_token()

                    self.token_repository.revoke_token(token_record)

                    self.token_repository.create_refresh_token(
                        user_id=user.id,
                        token_hash=hash_token(new_refresh_token),
                    )

                    return TokenResponse(
                        access_token=new_access_token,
                        refresh_token=new_refresh_token,
                        user=user,
                    )

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token недействителен",
        )