from api.schemas.propery_search_schema import SearchBase
from external_api.external_api_service import ApiService
from api.models.listing import Listing

# Get Listing
# async def get_listing(search_base: SearchBase) -> Listing:
async def get_listing(search_base: SearchBase):
    service: ApiService = ApiService(search_base)
    listings: list[Listing] = await service.get_listings()


