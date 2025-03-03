from fastapi import HTTPException, status, Response
from sqlalchemy import update
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import Optional
from api.schemas import UserCreate, UserUpdate
from ..models import User


# Create User
async def create_user(db: AsyncSession, user: UserCreate) -> User:
    try:
        # Check if user already exists, raise exception if they do
        user_exists: Optional[User] = await get_user_by_email(db, user.email)
        if user_exists:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='An account with this email may already exist.')

        # create user
        new_user: User = User(**user.model_dump())

        # Save to database
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
async def update_user(db: AsyncSession, user_id: int, user_update: UserUpdate) -> User:
    # Get user to update
    user: Optional[User] = await get_user(db, user_id)

    # Convert the update model into a dictionary, excluding fields not being updated
    updated_data: dict[str, str] = user_update.model_dump(exclude_unset=True)

    # If no updates provided return user as is
    if not updated_data:
        return user

    try:
        # Update the user  ORM object
        for key, value in updated_data.items():
            setattr(user, key, value)

        # commit changes
        await db.commit()
        await db.refresh(user)

        # Return updated user
        return user
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Duplicate entry detected")
    except SQLAlchemyError:
        await db.rollback()
        raise database_exception()


# Delete User
async def delete_user(db: AsyncSession, user_id: int) -> Response:
    # Get the user you want to delete
    user: User = await get_user(db, user_id)

    try:
        # Delete the user
        await db.delete(user)
        await db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)  # Response signifies deletion
    except SQLAlchemyError :
        await db.rollback()  # rollback db session prior to issue
        raise database_exception()


# Custom Exceptions
def database_exception()-> HTTPException:
    return HTTPException (status_code= status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'Database Error Occurred')


def user_not_found_exception() -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="No user found, register for an account and log in.",
        headers={"WWW-Authenticate": "Bearer"},  # Follows authentication standards
    )