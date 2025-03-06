from fastapi import APIRouter, Depends
from api.models import User
from api.schemas.listing_schema import ListingResponse, ListingBase
from api.schemas.propery_search_schema import SearchBase
from api.router.services.auth_services import get_authenticated_user
# from api.crud.listing_crud import get_listings
from external_api.external_api_service import ApiService
router = APIRouter(prefix='/listings')

@router.post('/', response_model=list[ListingResponse], status_code=200)
async def get_listings_route(search_base: SearchBase, authenticated_user: User = Depends(get_authenticated_user)) -> list[ListingResponse]:
    service = ApiService(search_base)
    listings =  await service.get_listings()
    return [ListingResponse.model_validate(listing, from_attributes=True) for listing in listings]
