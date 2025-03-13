from fastapi import HTTPException, status, Response
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from api.crud.user_crud import get_user
from api.schemas.propery_search_schema import SearchBase
from external_api.external_api_service import ApiService
from api.models import Listing, User


# Get All Listings
# async def get_listings(db: AsyncSession, user_id: int) ->  list[Listing]:
#     listings: list[Listing] = await db.execute(select(Listing).where(Listing.))




# Get Listings From External Api
async def get_listings_external_api(params: SearchBase) -> list[Listing]:
    service: ApiService = ApiService(params)
    return await service.get_listings_data()


# Get Single Listing From External Api
async def get_listing_external_api(zpid: int, params: SearchBase) -> Listing:
    service: ApiService = ApiService(params)
    return await service.get_listing_data_by_zpid(zpid)