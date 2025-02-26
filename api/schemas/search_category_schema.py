from pydantic import BaseModel
from typing import Optional

class LeadBase(BaseModel):
    name: str


class LeadCreate(LeadBase):
    pass


class LeadUpdate(BaseModel):
    name: Optional[str] = None


class LeadResponse(LeadBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True