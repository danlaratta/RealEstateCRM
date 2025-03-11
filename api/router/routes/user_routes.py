from fastapi import APIRouter, Depends, HTTPException, status, Response
from api.crud.user_crud import get_user, update_user, delete_user
from api.schemas.user_schema import UserResponse, UserUpdate
from sqlalchemy.ext.asyncio import AsyncSession
from api.database.database import get_db
from api.models.user import User
from ..services.auth_services import get_authenticated_user

# Define auth route
router = APIRouter(prefix='/user')

# Get User
@router.get('/{user_id}', response_model=UserResponse, status_code=200)
async def get_current_user(user_id: int, authenticated_user: User = Depends(get_authenticated_user), db: AsyncSession = Depends(get_db)) -> UserResponse:
    # Make sure user is authenticated
    if authenticated_user.id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='Access denied, can only update your own account.')
    
    # get the user by ID
    user: User = await get_user(db, user_id)
    return UserResponse.model_validate(user) # converts User model into UserResponse pydantic schema


# Update User
@router.put('/{user_id}', response_model=UserUpdate, status_code=200)
async def update_current_user(user_id: int, user_update: UserUpdate, authenticated_user: User = Depends(get_authenticated_user), db: AsyncSession = Depends(get_db)) -> UserResponse:
    # Make sure user is authenticated
    if authenticated_user.id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Access denied, can only update your own account.')

    # update and return user
    user: User = await update_user(db, user_id, user_update)
    return UserResponse.model_validate(user)


# Delete User
@router.delete('/{user_id}', status_code=204)
async def delete_current_user(user_id: int, authenticated_user: User = Depends(get_authenticated_user), db: AsyncSession = Depends(get_db)) -> Response:
    # Make sure user is authenticated
    if authenticated_user.id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='Access denied, can only update your own account.')

    # delete user and return 204 response code
    return await delete_user(db, user_id)
