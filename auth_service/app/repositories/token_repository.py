from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from ..models.refresh_token import RefreshToken


class TokenRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_refresh_token(
        self,
        user_id,
        token_hash: str,
        expires_days: int = 30,
    ):
        refresh_token = RefreshToken(
            user_id=user_id,
            token_hash=token_hash,
            expires_at=datetime.utcnow() + timedelta(days=expires_days),
        )

        self.db.add(refresh_token)
        self.db.commit()
        self.db.refresh(refresh_token)

        return refresh_token

    def get_active_tokens_by_user(self, user_id):
        return (
            self.db.query(RefreshToken)
            .filter(
                RefreshToken.user_id == user_id,
                RefreshToken.is_revoked == False,
                RefreshToken.expires_at > datetime.utcnow(),
            )
            .all()
        )

    def revoke_token(self, refresh_token: RefreshToken):
        refresh_token.is_revoked = True
        self.db.commit()
        self.db.refresh(refresh_token)

        return refresh_token