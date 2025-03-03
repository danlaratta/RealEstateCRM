from fastapi import APIRouter, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession
from api.database.database import get_db
from api.schemas.search_category_schema import CategoryCreate, CategoryResponse, CategoryUpdate
from api.models.user import User
from api.models.search_category import SearchCategory
from api.router.services.auth_services import get_authenticated_user
from api.crud.search_category_crud import create_category, get_category, get_all_categories, update_category, delete_category


router = APIRouter(prefix='/categories')


# Create Category
@router.post('/', response_model=CategoryCreate, status_code=201)
async def create_category_route(category_create: CategoryCreate,  authenticated_user: User = Depends(get_authenticated_user), db: AsyncSession = Depends(get_db)) -> CategoryResponse:
    new_category: SearchCategory = await create_category(db, authenticated_user.id, category_create)
    return CategoryResponse.model_validate(new_category)

# Get Single Category
@router.get('/{category_id}', response_model=CategoryResponse, status_code=200)
async def get_category_route(category_id: int, authenticated_user: User = Depends(get_authenticated_user), db: AsyncSession = Depends(get_db)) -> CategoryResponse:
    category: SearchCategory = await get_category(db, authenticated_user.id, category_id)
    return CategoryResponse.model_validate(category)


# Get All Categories
@router.get('/', response_model=list[CategoryResponse], status_code=200)
async def get_all_category_route(authenticated_user: User = Depends(get_authenticated_user), db: AsyncSession = Depends(get_db)) -> list[CategoryResponse]:
    categories: list[SearchCategory] = await get_all_categories(db, authenticated_user.id)
    return [CategoryResponse.model_validate(category) for category in categories]


# Update Category
@router.put('/{category_id}', response_model=CategoryUpdate, status_code=200)
async def update_category_route(category_id: int, category_update: CategoryUpdate, authenticated_user: User = Depends(get_authenticated_user), db: AsyncSession = Depends(get_db))  -> CategoryResponse:
    category: SearchCategory = await update_category(db, authenticated_user.id, category_id, category_update)
    return CategoryResponse.model_validate(category)


# Delete Category
@router.delete('/{category_id}', status_code=204)
async def delete_category_route(category_id: int, authenticated_user: User = Depends(get_authenticated_user), db: AsyncSession = Depends(get_db)) -> Response:
    return await delete_category(db, authenticated_user.id, category_id)



