from fastapi import HTTPException, status, Response
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from api.schemas.lead_schema import LeadCreate
from api.schemas.propery_search_schema import SearchBase
from api.models import Lead, User, Listing
from api.crud.user_crud import get_user
from api.crud.listing_crud import get_listing
from api.router.exceptions.exceptions import database_exception


async def create_lead_custom_search(db: AsyncSession, user_id: int, zpid: int, search_params: SearchBase, lead_create: LeadCreate) -> Lead:
    # Get User
    user: User = await get_user(db, user_id)

    # Convert search params into SearchBase
    try:
        params: SearchBase = SearchBase.model_validate(search_params)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'Invalid search params: {e}')

    # Get listings
    listing: Listing = await get_listing(zpid, search_params)

    if listing is None:
        raise HTTPException(status_code=404, detail="Facking Tits")

    # Create Lead
    lead: Lead = Lead(**lead_create.model_dump(exclude_unset=True), user_id=user.id, listing=listing)

    try:
        db.add(lead)
        await db.commit()
        await db.refresh(lead)
        return lead
    except IntegrityError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f'Lead already exists: str({e})')
    except SQLAlchemyError as e:
        await db.rollback()
        raise database_exception(e)



# Get All Leads
async def get_all_leads(db: AsyncSession, user_id: int) -> list[Lead]:
    result = await db.execute(select(Lead).filter(Lead.user_id == user_id))
    leads: list[Lead] = list[Lead](result.scalars().all())

    if leads is None or not leads:
        raise HTTPException(status_code=404, detail="No Leads found")

    return leads


# Get Lead
async def get_lead() -> Lead:
    pass


# Update Lead
async def update_lead() -> Lead:
    pass


# Delete Lead
async def delete_lead() -> Response:
    pass

