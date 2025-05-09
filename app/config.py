# config.py
"""
configuration settings

- google credentials
- fast api settings
- get firebase user from token

"""

from pathlib import Path
from functools import lru_cache

from typing import Annotated, Optional
from pydantic_settings import BaseSettings

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from firebase_admin.auth import verify_id_token


class Settings(BaseSettings):
    """Main settings"""

    app_name: str = "demofirebase"
    env: str = "development"
    frontend_url: str = "NA"
    google_application_credentials: str

    class Config:
        """
        .env
        """

        env_file = str(Path(__file__).resolve().parent.parent / ".env")


@lru_cache
def get_settings() -> Settings:
    """Settings

    Returns:
        Settings: list of settings
    """

    try:
        settings = Settings()
    except Exception as e:
        print("Failed to load settings:", e)
        raise
    return settings


# use of a simple bearer scheme as auth is handled by firebase and not fastapi
# we set auto_error to False because fastapi incorrectly returns a 403 intead
# of a 401
# see: https://github.com/tiangolo/fastapi/pull/2120
bearer_scheme = HTTPBearer(auto_error=False)


def get_firebase_user_from_token(
    token: Annotated[Optional[HTTPAuthorizationCredentials], Depends(bearer_scheme)],
) -> Optional[dict]:
    """Uses bearer token to identify firebase user id

    Args:
        token : the bearer token. Can be None as we set auto_error to False

    Returns:
        dict: the firebase user on success
    Raises:
        HTTPException 401 if user does not exist or token is invalid
    """

    try:
        if not token:
            # raise and catch to return 401, only needed because fastapi returns 403
            # by default instead of 401 so we set auto_error to False
            raise ValueError("No token")
        user = verify_id_token(token.credentials)
        return user

    # lots of possible exceptions, see firebase_admin.auth, but most of the time it is a credentials issue
    except Exception as exc:
        # see https://fastapi.tiangolo.com/tutorial/security/simple-oauth2/
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not logged in or Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc
