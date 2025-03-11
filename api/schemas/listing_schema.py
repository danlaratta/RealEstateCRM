from pydantic import BaseModel, Field
from typing import Optional


class ListingBase(BaseModel):
    zpid: int
    address: str
    status_type: str = Field(default='ForSale', alias='listingStatus')
    home_type: str =  Field(default='Houses', alias='propertyType')
    price: int
    bedrooms:int
    bathrooms: int
    square_ft: Optional[int] = Field(default=0, alias='livingArea')
    days_on_market: int = Field(default=0, alias='daysOnZillow')


class ListingCreate(ListingBase):
    pass


class ListingResponse(ListingBase):
    zpid:  int
    address: str
    status_type: str = Field(default='ForSale', alias='listingStatus')
    home_type: str = Field(default='Houses', alias='propertyType')
    price: int
    bedrooms: int
    bathrooms: int
    square_ft: Optional[int] = Field(default=0, alias='livingArea')
    days_on_market: int = Field(default=0, alias='daysOnZillow')
    # agent_id: int

    class Config:
        from_attributes = True
        populate_by_name = True
