from fastapi import HTTPException, status, Response
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from api.schemas.lead_schema import LeadCreate, LeadUpdate
from api.schemas.propery_search_schema import SearchBase
from api.models import Lead, User, Listing, PropertySearch
from api.crud.user_crud import get_user
from api.crud.listing_crud import get_listing_external_api
from api.crud.property_search_crud import get_search
from api.router.exceptions.exceptions import database_exception
from typing import Optional


# Create Lead - Manual/Unsaved Search
async def create_lead_manual_search(db: AsyncSession, user_id: int, zpid: int, search_params: SearchBase, lead_create: LeadCreate) -> Lead:
    # Get User
    user: User = await get_user(db, user_id)

    # Get listings
    listing: Listing = await get_listing_external_api(zpid, search_params)

    if listing is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Listing with zpid: {zpid} does not exist')

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


# Create Lead - Saved Search
async def create_lead_saved_search(db: AsyncSession, user_id: int, zpid: int, search_id: int, lead_create: LeadCreate) -> Lead:
        # Get User
        user: User = await get_user(db, user_id)

        # Get Saved Search and convert to SearchBase
        search: PropertySearch = await get_search(db, user_id, search_id)
        search_params: SearchBase = SearchBase.model_validate(search)

        # Get listings
        listing: Listing = await get_listing_external_api(zpid, search_params)

        if listing is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f'Listing with zpid: {zpid} does not exist')

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
    result = await db.execute(select(Lead).where(Lead.user_id == user_id))
    leads: list[Lead] = list[Lead](result.scalars().all())

    if leads is None or not leads:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No Leads found")

    return leads


# Get Lead
async def get_lead(db: AsyncSession, user_id: int, lead_id: int) -> Lead:
    result = await db.execute(select(Lead).where(Lead.id == lead_id, Lead.user_id == user_id))
    lead: Optional[Lead] = result.scalar_one_or_none()
    return lead


# Get all listings from leads
async def get_all_listings_from_leads(db: AsyncSession, user_id: int) -> list[Lead]:
    # eager join (preloads related data in a single query) the listing relationship using (all the listings asscociated with leads)
    result = await db.execute(select(Lead).options(joinedload(Lead.listing)).where(Lead.user_id == user_id))
    listings: list[Lead] = list[Lead](result.scalars().unique().all())
    return listings


# Get a listing from a lead
async def get_listing_from_lead(db: AsyncSession, user_id: int,  lead_id: int) -> Lead:
    result = await db.execute(select(Lead).options(joinedload(Lead.listing)).where(Lead.user_id == user_id, Lead.id == lead_id))
    lead: Optional[Lead] = result.scalar_one_or_none()
    return lead


# Update Lead
async def update_lead(db: AsyncSession, user_id: int, lead_id: int, lead_update: LeadUpdate) -> Lead:
    # Get Lead to update
    lead: Lead = await get_lead(db, user_id, lead_id)

    try:
        for key, value in lead_update.model_dump(exclude_unset=True).items():
            setattr(lead, key, value)

        await db.commit()
        await db.refresh(lead)
        return lead
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Duplicate entry detected')
    except SQLAlchemyError as e:
        await db.rollback()
        raise database_exception(e)


# Delete Lead
async def delete_lead(db: AsyncSession, user_id: int, lead_id: int) -> Response:
    # Get Lead to delete
    lead: Lead = await get_lead(db, user_id, lead_id)

    try:
        await db.delete(lead)
        await db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except SQLAlchemyError as e:
        await db.rollback()
        raise database_exception(e)


