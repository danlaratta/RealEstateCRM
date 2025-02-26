from pydantic import BaseModel
from typing import Optional

class LeadBase(BaseModel):
    first_name: str
    last_name: str
    phone: str
    email: str
    password: str


class LeadCreate(LeadBase):
    pass


class LeadUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None


class LeadResponse(LeadBase):
    id: int

    class Config:
        from_attributes = True