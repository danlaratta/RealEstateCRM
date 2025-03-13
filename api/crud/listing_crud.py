from api.schemas.propery_search_schema import SearchBase
from external_api.external_api_service import ApiService
from api.models import Listing


# Get Listings From External Api
async def get_listings_external_api(params: SearchBase) -> list[Listing]:
    service: ApiService = ApiService(params)
    return await service.get_listings_data()


# Get Single Listing From External Api
async def get_listing_external_api(zpid: int, params: SearchBase) -> Listing:
    service: ApiService = ApiService(params)
    return await service.get_listing_data_by_zpid(zpid)