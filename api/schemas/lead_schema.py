from pydantic import BaseModel
from typing import Optional

class LeadBase(BaseModel):
    status: str
    interest_level: str


class LeadCreate(LeadBase):
    pass


class LeadUpdate(BaseModel):
    status: Optional[str] = None
    interest_level: Optional[str] = None


class LeadResponse(LeadBase):
    id: int
    user_id: int
    listing_id: int

    class Config:
        from_attributes = True