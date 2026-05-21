from fastapi import Header, HTTPException, status
from jose import JWTError, jwt

from .config import settings


def verify_jwt_token(
    authorization: str = Header(default=None),
):
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token отсутствует",
        )

    try:
        token = authorization.replace("Bearer ", "")

        payload = jwt.decode(
            token,
            settings.jwt_secret_key,
            algorithms=[settings.jwt_algorithm],
        )

        return payload

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Невалидный токен",
        )from fastapi import Header, HTTPException, status
from jose import JWTError, jwt

from .config import settings


def verify_jwt_token(
    authorization: str = Header(default=None),
):
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token отсутствует",
        )

    try:
        token = authorization.replace("Bearer ", "")

        payload = jwt.decode(
            token,
            settings.jwt_secret_key,
            algorithms=[settings.jwt_algorithm],
        )

        return payload

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Невалидный токен",
        )