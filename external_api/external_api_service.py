from api.schemas.propery_search_schema import SearchBase
from api.schemas.listing_schema import ListingCreate
from fastapi import HTTPException, status
from typing import Any
import requests
from dotenv import load_dotenv
import os
from api.models.listing import Listing

class ApiService:
    def __init__(self, params: SearchBase):
        load_dotenv()
        self.API_KEY = os.getenv('API_KEY')
        self.HOST = os.getenv('HOST')
        self.BASE_URL = os.getenv('BASE_URL')
        self.headers = {'x-rapidapi-key': self.API_KEY, 'x-rapidapi-host': self.HOST}
        self.params = params


    def validate_params(self):
        # All params are required, check if any attribute is None or an empty value
        missing_params = [param for param, value in vars(self.params).items() if value is None]

        if missing_params:
            raise HTTPException(
                status_code=400,
                detail=f'Missing required fields: {', '.join(missing_params)}'
            )


    # Get json from api
    async def get_json_listings(self) -> dict[str, list[dict[str, Any]]]:
        try:
            response = requests.get(self.BASE_URL, headers=self.headers, params=self.params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'API request failed: {str(e)}')


    # Get listings
    async def get_listings_data(self) -> list[Listing]:
        json_data = await self.get_json_listings()

        # Extract the list of property listings from the API response
        listings_data = json_data.get('props', [])

        # Convert raw listing data into ListingCreate instances
        listing_create_instances = [ListingCreate.model_validate(listing) for listing in listings_data]

        # Convert ListingCreate instances into Listing model instances for database storage
        listings = [Listing(**listing.model_dump()) for listing in listing_create_instances]

        return listings


    # Get listing by zpid
    async def get_listing_data_by_zpid(self, zpid: int) -> Listing:
        listings: list[Listing] = await self.get_listings_data()  # Get all listings

        for listing in listings:
            if listing.zpid == zpid:
                return listing

        raise HTTPException(status_code=404, detail="Listing not found")