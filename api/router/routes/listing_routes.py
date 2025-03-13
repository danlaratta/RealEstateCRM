from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.models import User, Listing
from api.schemas.listing_schema import ListingResponse
from api.schemas.propery_search_schema import SearchBase
from api.router.services.auth_services import get_authenticated_user
from api.crud.listing_crud import get_listings_external_api, get_listing_external_api
from api.database.database import get_db

router = APIRouter(prefix='/listings')


# Get all listings for a specific search
@router.post('/', response_model=list[ListingResponse], status_code=200)
async def get_listings_route(params: SearchBase, authenticated_user: User = Depends(get_authenticated_user)) -> list[ListingResponse]:
    listings: list[Listing] = await get_listings_external_api(params)
    return [ListingResponse.model_validate(listing) for listing in listings]


# Get a listing by zpid for a specific search
@router.post('/{zpid}', response_model=ListingResponse, status_code=200)
async def get_listing_route(zpid: int, params: SearchBase, authenticated_user: User = Depends(get_authenticated_user)) -> ListingResponse:
    listing: Listing = await get_listing_external_api(zpid, params)
    return ListingResponse.model_validate(listing)