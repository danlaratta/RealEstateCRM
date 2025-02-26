from pydantic import BaseModel

class ListingBase(BaseModel):
    address: str
    price: int
    beds: int
    baths: int
    square_ft: int
    days_on_market: int


class ListingCreate(ListingBase):
    pass


class ListingResponse(ListingBase):
    id: int
    agent_id: int

    class Config:
        from_attributes = True