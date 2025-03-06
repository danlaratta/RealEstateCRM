from pydantic import BaseModel, Field
from typing import Optional

class ListingBase(BaseModel):
    address: str
    status_type: str = 'New'
    home_type: str = 'House'
    price: int
    bedrooms: int = Field(default=0, alias='beds')
    bathrooms: int = Field(default=0, alias='baths')
    square_ft: int = Field(default=0, alias='livingArea')
    days_on_market: int = Field(default=0, alias='daysOnZillow')


class ListingCreate(ListingBase):
    pass


class ListingResponse(ListingBase):
    id: Optional[int]
    address: str
    status_type: str = 'ForSale'
    home_type: str = 'houses'
    price: int
    bedrooms: int = Field(default=0, alias='beds')
    bathrooms: int = Field(default=0, alias='baths')
    square_ft: int = Field(default=0, alias='livingArea')
    days_on_market: int = Field(default=0, alias='daysOnZillow')
    # agent_id: int

    class Config:
        from_attributes = True
