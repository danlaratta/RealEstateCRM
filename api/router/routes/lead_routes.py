from fastapi import APIRouter, Depends, Response, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from api.models import User, Lead
from api.crud.lead_crud import create_lead_custom_search, get_all_leads
from api.schemas.lead_schema import LeadResponse, LeadCreate
from api.router.services.auth_services import get_authenticated_user
from api.database.database import get_db


router = APIRouter(prefix='/leads')


# Create Lead from custom search
@router.post('/custom-search', response_model=LeadResponse, status_code=200)
async def get_lead_route(request_body: dict, authenticated_user: User = Depends(get_authenticated_user), db: AsyncSession = Depends(get_db)) -> LeadResponse:
    # extract parmas from request body
    try:
        zpid = request_body.get('zpid')
        search_params = request_body.get('search_params')
        lead_data = request_body.get('lead_create')

        if not zpid or not search_params or not lead_data:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Missing one of the required fields: zpid, search_params, or lead_create')

        # Convert search params and lead_create to schemas
        lead_create: LeadCreate = LeadCreate.model_validate(lead_data)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail= f'Invalid request format: {str(e)}')

    lead: Lead = await create_lead_custom_search(db, authenticated_user.id, zpid, search_params, lead_create)
    return LeadResponse.model_validate(lead)


# Get all Leads
@router.get('/', response_model=list[LeadResponse], status_code=200)
async def get_leads_route(authenticated_user: User = Depends(get_authenticated_user), db: AsyncSession = Depends(get_db)) -> list[LeadResponse]:
    leads: list[Lead] = await get_all_leads(db, authenticated_user.id)
    return [LeadResponse.model_validate(lead) for lead in leads]


# Get a Lead
@router.get('/{zpid}', response_model=LeadResponse, status_code=200)
async def get_lead_route(authenticated_user: User = Depends(get_authenticated_user), db: AsyncSession = Depends(get_db)) -> LeadResponse:
    pass


# Update Lead
@router.put('/{zpid}', response_model=LeadResponse, status_code=200)
async def update_lead_route(authenticated_user: User = Depends(get_authenticated_user), db: AsyncSession = Depends(get_db)) -> LeadResponse:
    pass


# Delete Lead
@router.delete('/{zpid}', response_model=LeadResponse, status_code=200)
async def delete_lead_route(authenticated_user: User = Depends(get_authenticated_user), db: AsyncSession = Depends(get_db)) -> Response:
    pass
