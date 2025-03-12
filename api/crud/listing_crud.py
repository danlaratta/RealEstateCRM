from api.schemas.propery_search_schema import SearchBase
from external_api.external_api_service import ApiService
from api.models import Listing, User


# Get Listings
async def get_listings(params: SearchBase) -> list[Listing]:
    service: ApiService = ApiService(params)
    return await service.get_listings_data()


# Get Single Listing
async def get_listing(zpid: int, params: SearchBase) -> Listing:
    service: ApiService = ApiService(params)
    return await service.get_listing_data_by_zpid(zpid)