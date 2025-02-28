from fastapi import Depends, HTTPException, status, APIRouter
from api.crud.user_crud import get_user
from api.schemas.user_schema import UserResponse
from sqlalchemy.ext.asyncio import AsyncSession
from api.database.database import get_db

# Define auth route
router = APIRouter(prefix='/user')

@router.get('/{user_id}', response_model=UserResponse)
async def get_current_user(user_id: int, db: AsyncSession = Depends(get_db)):
    user = await get_user(db, user_id)

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User is not found something wrong')
    return user
