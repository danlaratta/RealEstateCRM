from jose import jwt
from passlib.exc import InvalidTokenError
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime, UTC
from jose.exceptions import JWTError
from api.database import get_db
from api.models import User
from fastapi import Depends, HTTPException, status
from datetime import timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from api.crud.user_crud import get_user, get_user_by_email
from ..config import (SECRET_KEY, ALGORITHM, bcrypt_context, oauth2_scheme)


# Hash password
def get_hashed_password(password: str) -> str:
    return bcrypt_context.hash(password)


# Verify hashed password matches user's password
def verify_password(password: str, hashed_pwd: str) -> bool:
    return bcrypt_context.verify(password, hashed_pwd)


# Authenticate User
async def authenticate_user(email: str, password: str, db: AsyncSession = Depends(get_db)) -> User:
    try:
        user: User = await get_user_by_email(db, email)
    except SQLAlchemyError as e:  # Catch database-related errors
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=bad_request_exception(e)
        )

    if not user or not verify_password(password, user.password):
        raise credential_exception()

    return user


# Create new JWT Token
def create_access_token(email: str, user_id: int, expires_delta: timedelta or None = None) -> str:
    to_encode = {'sub': email, 'id': user_id}
    expires = datetime.now(UTC) + (expires_delta if expires_delta else timedelta(minutes=30))
    to_encode.update({
        'exp': expires,
        'iat': datetime.now(UTC)
    })

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# Get current user and validate their JWT Token, used to protect routes that requires a user to be logged in
async def get_authenticated_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)) -> User:
    try:
        # Decode token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        # Extract email and user_id from Token
        email: str = payload.get('sub')
        user_id: str = payload.get('id')

        if email is None:
            raise credential_exception()
    except (InvalidTokenError, JWTError):
        raise credential_exception()

    # Get and return valid user
    user: User = await get_user(db, int(user_id))
    if user is None:
        raise credential_exception()
    return user


# Custom Exception
def credential_exception() -> HTTPException:
    return HTTPException( status_code= status.HTTP_401_UNAUTHORIZED, detail='Invalid credentials', headers={'WWW-Authenticate': 'Bearer'} )

def bad_request_exception(e) -> HTTPException:
    return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'Unable to Login: {e}')