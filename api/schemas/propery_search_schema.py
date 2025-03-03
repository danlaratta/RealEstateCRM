from pydantic import BaseModel
from typing import Optional

class SearchBase(BaseModel):
    city: str
    state: str
    price_min: int
    price_max: int
    beds: int
    baths: int
    square_ft_min: int
    square_ft_max: int


class SearchCreate(SearchBase):
    pass


class SearchUpdate(BaseModel):
    city: Optional[str] = None
    state: Optional[str] = None
    price_min: Optional[int] = None
    price_max: Optional[int] = None
    beds: Optional[int] = None
    baths: Optional[int] = None
    square_ft_min: Optional[int] = None
    square_ft_max: Optional[int] = None


class SearchResponse(SearchBase):
    id: int
    user_id: int
    category_id: int

    class Config:
        from_attributes = True