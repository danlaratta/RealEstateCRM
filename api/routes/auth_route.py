from datetime import timedelta
from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt
from passlib.context import CryptContext
from passlib.exc import InvalidTokenError
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, UTC
from ..database import get_db
from ..models import User
from ..crud.user_crud import create_user, get_user, get_user_by_email
from ..schemas.user_schema import UserResponse, UserCreate, Token
from jose.exceptions import JWTError
import os

# Get secret key
load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY')
if not SECRET_KEY:
    raise Exception('Secret Key does not exist')

# JWT configurations
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Define auth route
router = APIRouter(prefix='/auth')

# Initialize bcrypt password hashing
bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

# Set up OAuth2 for receiving JWT Tokens
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='auth/login')


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
    except:
        raise bad_request_exception()

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

def bad_request_exception() -> HTTPException:
    return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Unable to register')