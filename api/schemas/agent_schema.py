from pydantic import BaseModel
from typing import Optional

class AgentBase(BaseModel):
    first_name: str
    last_name: str
    phone: str
    email: str


class AgentCreate(AgentBase):
    pass


class AgentUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None


class AgentResponse(AgentBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True