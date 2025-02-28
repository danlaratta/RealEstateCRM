from dotenv import load_dotenv
from fastapi import APIRouter
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
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