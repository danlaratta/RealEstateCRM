from fastapi import HTTPException, status, Response
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import Optional
from starlette.status import HTTP_404_NOT_FOUND
from api.models import User, PropertySearch, SearchCategory
from api.crud.user_crud import get_user
from api.crud.search_category_crud import get_category
from api.schemas.propery_search_schema import SearchCreate, SearchUpdate
from api.router.exceptions.exceptions import database_exception

# Create Search
async def create_search(db: AsyncSession, user_id: int, search_create: SearchCreate) -> PropertySearch:
    # Get User
    user: User = await get_user(db, user_id)

    # Get Search Category
    category: SearchCategory = await get_category(db, user_id, search_create.category_id)

    # Create Search
    new_search: PropertySearch = PropertySearch(**search_create.model_dump(),  user_id = user.id, category= category)

    try:
        db.add(new_search)
        await db.commit()
        await db.refresh(new_search)
        return new_search
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Search already exists")
    except SQLAlchemyError as e:
        await db.rollback()
        raise database_exception(e)


# Get Search
async def get_search(db: AsyncSession, user_id: int, search_id) -> PropertySearch:
    # Query for a Search
    result = await db.execute(select(PropertySearch).filter(PropertySearch.id == search_id, PropertySearch.user_id == user_id))
    search: Optional[PropertySearch] = result.scalar_one_or_none()

    if search is None:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail='No saved search found')

    return search


# Get All Searches
async def get_all_searches(db: AsyncSession, user_id: int) -> list[PropertySearch]:
    # Query for all Searches
    result = await db.execute(select(PropertySearch).filter(PropertySearch.user_id == user_id))
    searches: list[PropertySearch] = list[PropertySearch](result.scalars().all())

    if searches is None:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail='No Searches Found')

    return searches


# Update Search
async def update_search(db: AsyncSession, user_id: int, search_id: int, search_update: SearchUpdate) -> PropertySearch:
    # Get Search to update
    search: PropertySearch = await get_search(db, user_id, search_id)

    try:
        # Get the udpated data
        update_data = search_update.model_dump(exclude_unset=True)

        # Handle updating the PropertySearch and SearchCategory relationship (has to be done separately from attributes)
        if "category_id" in update_data:
            category: SearchCategory = await get_category(db, user_id, update_data["category_id"])
            search.category = category  # Set the relationship
            del update_data["category_id"]  # Remove category_id from update_data so it's not updated again when updating the attributes

        # Update remaining fields
        for key, value in update_data.items():
            setattr(search, key, value)

        await db.commit()
        await db.refresh(search)
        return search
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Search already exists")
    except SQLAlchemyError as e:
        await db.rollback()
        raise database_exception(e)



# Delete Search
async def delete_search(db: AsyncSession, user_id: int, search_id: int) -> Response:
    # Get Search to delete
    search: PropertySearch = await get_search(db, user_id, search_id)

    try:
        await db.delete(search)
        await db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except SQLAlchemyError as e:
        await db.rollback()
        raise database_exception(e)



