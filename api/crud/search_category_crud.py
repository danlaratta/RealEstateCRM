from fastapi import HTTPException, status, Response
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import Optional
from api.schemas.search_category_schema import CategoryCreate, CategoryUpdate
from ..models import SearchCategory, User
from ..crud.user_crud import get_user
from ..router.exceptions import database_exception

# Create Category
async def create_category(db: AsyncSession, user_id: int, category_create: CategoryCreate) -> SearchCategory:
    # Get User and create SearchCategory
    user: User = await get_user(db, user_id)
    new_category: SearchCategory = SearchCategory(**category_create.model_dump(), user_id = user.id)

    try:
        db.add(new_category)
        await db.commit()
        await db.refresh(new_category)
        return new_category
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Category already exists")
    except SQLAlchemyError as e:
        await db.rollback()
        raise database_exception(e)


# Get Single Category
async def get_category(db: AsyncSession, user_id: int, category_id: int) -> SearchCategory:
    # Query for specific category
    result = await db.execute(select(SearchCategory).where(SearchCategory.id == category_id, SearchCategory.user_id == user_id))
    category: Optional[SearchCategory] = result.scalar_one_or_none()

    if category is None:
        raise HTTPException(status_code=404, detail="Search Category not found")

    return category


# Get All Categories
async def get_all_categories(db: AsyncSession, user_id: int) -> list[SearchCategory]:
    # Query for all categories
    result = await db.execute(select(SearchCategory).where(SearchCategory.user_id == user_id))
    categories: list[SearchCategory] = list[SearchCategory](result.scalars().all())

    if categories is None:
        raise HTTPException(status_code=404, detail="No Search Categories found")

    return categories


# Update Category
async def update_category(db: AsyncSession, user_id: int, category_id: int, category_update: CategoryUpdate) -> SearchCategory:
    # Get category to update
    category: SearchCategory = await get_category(db, user_id, category_id)

    try:
        for key, value in category_update.model_dump(exclude_unset=True).items():
            setattr(category, key, value)

        await db.commit()
        await db.refresh(category)
        return category
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Duplicate entry detected")
    except SQLAlchemyError as e:
        await db.rollback()
        raise database_exception(e)


# Delete Category
async def delete_category(db: AsyncSession, user_id: int, category_id: int) -> Response:
    # Get category to delete
    category: SearchCategory = await get_category(db, user_id, category_id)

    try:
        await db.delete(category)
        await db.commit()
        return Response(status_code= status.HTTP_204_NO_CONTENT)
    except SQLAlchemyError as e:
        await db.rollback()
        raise database_exception(e)

