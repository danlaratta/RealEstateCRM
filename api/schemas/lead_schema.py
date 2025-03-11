from pydantic import BaseModel, Field
from datetime import datetime, UTC

class LeadBase(BaseModel):
    zpid: int
    status: str = Field(default='New')
    interest_level: str = Field(default='No Interest')
    date_saved: datetime = Field(default=datetime.now(UTC))


class LeadCreate(LeadBase):
    pass


class LeadUpdate(BaseModel):
    status: str = Field(default='New')
    interest_level: str = Field(default='No Interest')


class LeadResponse(LeadBase):
    id: int
    user_id: int
    zpid: int
    date_saved: datetime = Field(default=datetime.now(UTC))
    status: str = Field(default='New')
    interest_level: str = Field(default='No Interest')


    class Config:
        from_attributes = True