from pydantic import BaseModel
from typing import Optional

class SearchCategoryBase(BaseModel):
    name: str


class SearchCategoryCreate(SearchCategoryBase):
    pass


class SearchCategoryUpdate(BaseModel):
    name: Optional[str] = None


class SearchCategoryResponse(SearchCategoryBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True