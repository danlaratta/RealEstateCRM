from fastapi import HTTPException, status
from sqlalchemy import update
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from passlib.context import CryptContext
from api.schemas import UserCreate, UserUpdate
from ..models import User
from typing import Optional


# Initialize bcrypt password hashing
bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


# Create User
async def create_user(db: AsyncSession, user: UserCreate) -> User:
    try:
        # Check if user already exists, raise exception if they do
        user_exists: Optional[User] = await get_user_by_email(db, user.email)
        if user_exists:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='An account with this email may already exist.')

        # create user
        new_user: User = User(**user.model_dump())

        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)
    except IntegrityError:  # Handle unique constraint violations
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already exists")
    except SQLAlchemyError :
        await db.rollback()  # Ensure rollback on failure
        raise database_exception()  # Custom database error handling

    return new_user


# Get User by ID
async def get_user(db: AsyncSession, user_id: int) -> User:
    user: Optional[User] = await db.get(User, user_id) # function may return none so type is an Optional

    if user is None:
        raise user_not_found_exception()

    return user


# Get User by email/username
async def get_user_by_email(db: AsyncSession, email: str) -> User:
    try:
        result = await db.execute(select(User).filter(User.email == email))
        user: Optional[User] = result.scalar_one_or_none()

    except SQLAlchemyError :
        raise database_exception()

    return user # will return User or None depending on if the user exists or not


# Update User
async def update_user(db: AsyncSession, user_update_id, user_update: UserUpdate) -> User:
    # Get user to update
    user: User = await get_user(db, user_update_id)

    # Convert pydantic schema to dictionary  only updates the attributes provided in the request from FE (exclude_unset=True)
    update_data = user_update.model_dump(exclude_unset=True)

    try:
        # Update user
        await db.execute(update(User).where(User.id == user_update_id).values(**update_data))

        # Save changes to database
        await db.commit()
        await db.refresh(user)
    except SQLAlchemyError :
        await db.rollback() # rollback db session prior to issue
        raise database_exception()

    return user


# Delete User
async def delete_user(db: AsyncSession, user_id: int) -> User:
    # Get the user you want to delete
    user: User = await get_user(db, user_id)

    try:
        # Delete the user
        await db.delete(user)
        await db.commit()
    except SQLAlchemyError :
        await db.rollback()  # rollback db session prior to issue
        raise database_exception()

    return user


# Custom Exceptions
def database_exception()-> HTTPException:
    return HTTPException (status_code= status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'Database Error Occurred')


def user_not_found_exception() -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="No user found, register for an account and log in.",
        headers={"WWW-Authenticate": "Bearer"},  # Follows authentication standards
    )