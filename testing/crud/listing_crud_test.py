import pytest
from unittest.mock import AsyncMock, patch
from api.crud.lead_crud import create_lead_custom_search
from api.schemas.lead_schema import LeadCreate
from api.models import User, PropertySearch, Listing, Lead
from external_api.external_api_service import ApiService
from api.crud.listing_crud import get_listing

@pytest.mark.asyncio
async def test_get_listing(mocker):
    # Model Mocks
    zpid= 35453710
    mock_listing: Listing = Listing(zpid= 35453710, address= '2089 13th St SW, Akron, OH 44314', status_type= 'FOR_SALE', home_type= 'SINGLE_FAMILY', price= 110000, bedrooms= 3, bathrooms= 2, square_ft= 920, days_on_market= 2)
    params = {
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
    }

    # Mock ApiService
    with patch("external_api.external_api_service.ApiService") as MockApiService:
        mock_service = MockApiService.return_value
        mock_service.get_listing_data_by_zpid = AsyncMock(return_value=mock_listing)

        result = await get_listing(zpid, params)

        assert result.address == mock_listing.address
        MockApiService.assert_called_once_with(params)
        mock_service.get_listing_data_by_zpid.assert_called_once_with(zpid)

