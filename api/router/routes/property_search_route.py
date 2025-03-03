from fastapi import APIRouter, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession
from api.schemas.propery_search_schema import SearchResponse, SearchCreate, SearchUpdate
from api.models import User, PropertySearch
from api.crud.property_search_crud import create_search, get_search, get_all_searches, update_search, delete_search
from api.database.database import get_db
from api.router.services.auth_services import get_authenticated_user

router = APIRouter(prefix='/searches')

# Create Search
@router.post('/', response_model=SearchResponse, status_code=201)
async def create_search_route(search_create: SearchCreate, authenticated_user: User = Depends(get_authenticated_user), db: AsyncSession = Depends(get_db)) -> SearchResponse:
    search: PropertySearch = await create_search(db, authenticated_user.id, search_create)
    return SearchResponse.model_validate(search)


# Get Search
@router.get('/{search_id}', response_model=SearchResponse, status_code=200)
async def get_search_route(search_id: int, authenticated_user: User = Depends(get_authenticated_user), db: AsyncSession = Depends(get_db)) -> SearchResponse:
    search: PropertySearch = await get_search(db, authenticated_user.id, search_id)
    return SearchResponse.model_validate(search)


# Get All Search
@router.get('/', response_model=list[SearchResponse], status_code=200)
async def get_all_search_route(authenticated_user: User = Depends(get_authenticated_user), db: AsyncSession = Depends(get_db)) -> list[SearchResponse]:
    searches: list[PropertySearch] = await get_all_searches(db, authenticated_user.id)
    return [SearchResponse.model_validate(search) for search in searches]

# Update Search
@router.put('/{search_id}', response_model=SearchResponse, status_code=200)
async def update_search_route(search_id: int, search_update: SearchUpdate, authenticated_user: User = Depends(get_authenticated_user), db: AsyncSession = Depends(get_db)) -> SearchResponse:
    search: PropertySearch = await update_search(db, authenticated_user.id, search_id, search_update)
    return SearchResponse.model_validate(search)


# Delete Search
@router.delete('/{search_id}', status_code=204)
async def delete_search_route(search_id: int, authenticated_user: User = Depends(get_authenticated_user), db: AsyncSession = Depends(get_db)) -> Response:
    return await delete_search(db, authenticated_user.id, search_id)
