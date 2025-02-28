from datetime import timedelta
from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from api.database import get_db
from api.models import User
from api.crud.user_crud import create_user
from api.schemas.user_schema import UserResponse, UserCreate, Token
from ..config import (ACCESS_TOKEN_EXPIRE_MINUTES, bcrypt_context)
from ..services import ( authenticate_user, create_access_token, credential_exception)


# Define auth route
router = APIRouter(prefix='/auth')

# Register a user
@router.post('/register', response_model=UserResponse)
async def register_user(user: UserCreate, db: AsyncSession = Depends(get_db)) -> User:
    try:
        # If user doesn't exist hash password and create user
        user.password = bcrypt_context.hash(user.password)

        # Create and return the user
        new_user = await create_user(db, user)
    except HTTPException as e:
        raise e  # Preserve meaningful exceptions (e.g., user already exists)
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Unexpected error during registration")


    return new_user


@router.post('/login', response_model=Token)
async def login_user(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)) -> dict[str: str]:
    try:
        # get authenticated user
        user: User = await authenticate_user(form_data.username, form_data.password, db)
    except HTTPException as e:
        raise e  # Reraise only known exceptions
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Unexpected error during login")

    if not user:
        raise credential_exception()

    access_token_exp: timedelta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(user.email, user.id, access_token_exp)

    return {'access_token': access_token, 'token_type': 'bearer', 'email': user.email}
