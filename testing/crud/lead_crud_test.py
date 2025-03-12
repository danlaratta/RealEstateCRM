import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from unittest.mock import AsyncMock, patch
from api.crud.lead_crud import create_lead_manual_search
from api.schemas.lead_schema import LeadCreate
from api.models import User, PropertySearch, Listing, Lead

@pytest.mark.asyncio
async def test_create_lead_saved_search(mocker):
    # Mock database session
    mock_db = AsyncMock(spec=AsyncSession)
    
    # Model Mocks
    user_mock: User = User(id=1, first_name='Dan', last_name='Laratta', phone=1234567890, email='dan@gmail.com', password='dan123')
    search_mock: PropertySearch = PropertySearch(id=1, location= 'akron, ohio', status_type= 'ForSale', home_type= 'Houses', price_max= 120000, baths_min= 2, baths_max= 2, beds_min= 3, beds_max= 3, square_ft_min= 750, square_ft_max= 1250)
    listing_mock: Listing = Listing(zpid= 35453710, address= '2089 13th St SW, Akron, OH 44314', status_type= 'FOR_SALE', home_type= 'SINGLE_FAMILY', price= 110000, bedrooms= 3, bathrooms= 2, square_ft= 920, days_on_market= 2)

    # Mock DB Get Functions
    mocker.patch('api.crud.user_crud.get_user', return_value=user_mock)
    mocker.patch('api.crud.property_search_crud.get_search', return_value=search_mock)

    # Mock ApiService
    mock_service = mocker.patch('external_api.external_api_service.ApiService')
    mock_service.return_value.get_listing_by_zpid.return_value = listing_mock


    #
    request_body: dict = {
        "zpid": 35453710,
        "search_params": {
            "location": "akron, ohio",
            "status_type": "ForSale",
            "home_type": "Houses",
            "baths_min": 2,
            "baths_max": 2,
            "beds_min": 3,
            "beds_max": 3,
            "square_ft_min": 750,
            "square_ft_max": 1500,
            "price_max": 120000
        },
        "lead_create": {
            "zpid": 35453710,
            "user_id": 1,
            "status": "New",
            "interest_level": "High"
        }
    }

    # Extract params from request body
    zpid = request_body.get('zpid')
    search_params = request_body.get('search_params')
    lead_create = request_body.get('lead_create')

    # Mock Lead
    lead_create_mock: LeadCreate = LeadCreate.model_validate(lead_create)

    # Call Create Crud Func
    lead_mock: Lead = await create_lead_manual_search(mock_db, user_mock.id,zpid, search_params, lead_create_mock)

    print(f'Lead Mock zpid: {lead_mock.zpid}')
    print(f'Listing Mock zpid: {listing_mock.zpid}')
    print(f'Lead Mock status: {lead_mock.status}')
    print(f'Lead Mock interest level: {lead_mock.interest_level}')

    # Assertions
    assert lead_mock.zpid == listing_mock.zpid
    assert lead_mock.status == 'New'
    assert lead_mock.interest_level == 'High'

    # Verify DB commit and refresh were called
    mock_db.add.assert_called_once()
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once_with(lead_mock)