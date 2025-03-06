from pydantic import BaseModel, Field, computed_field
from typing import Optional
from api.schemas.search_category_schema import CategoryResponse


class SearchBase(BaseModel):
    # city: str
    # state: str
    location: str
    status_type: str
    home_type: str = Field(default='houses', alias='propertyType')
    price_min: Optional[int] = Field(default=0, alias='priceMin')
    price_max: Optional[int] = Field(default=0, alias='priceMax')
    beds_min: Optional[int] = Field(default=0, alias='bedsMin')
    beds_max: Optional[int] = Field(default=0, alias='bedsMax')
    baths_min: Optional[int] = Field(default=0, alias='bathsMin')
    baths_max: Optional[int] = Field(default=0, alias='bathsMax')
    square_ft_min: Optional[int] = Field(default=0, alias='sqftMin')
    square_ft_max: Optional[int] = Field(default=0, alias='sqftMax')

    # Creates location property (required for external api search paramter)
    # @computed_field
    # @property
    # def location(self) -> str:
    #     return f'{self.city}, {self.state}'


class SearchCreate(SearchBase):
    category_id: int  # Ensure category is required when creating a search


class SearchUpdate(BaseModel):
    # city: Optional[str] = None
    # state: Optional[str] = None
    location: str
    status_type: Optional[str] = None
    home_type: Optional[str] = None
    price_min: Optional[int] = Field(default=0, alias='priceMin')
    price_max: Optional[int] = Field(default=0, alias='priceMax')
    beds_min: Optional[int] = Field(default=0, alias='bedsMin')
    beds_max: Optional[int] = Field(default=0, alias='bedsMax')
    baths_min: Optional[int] = Field(default=0, alias='bathsMin')
    baths_max: Optional[int] = Field(default=0, alias='bathsMax')
    square_ft_min: Optional[int] = Field(default=0, alias='sqftMin')
    square_ft_max: Optional[int] = Field(default=0, alias='sqftMax')

    # @computed_field
    # @property
    # def location(self) -> str:
    #     return f'{self.city}, {self.state}'


class SearchResponse(SearchBase):
    id: int
    user_id: int
    category: 'CategoryResponse' # Include the category details (uses string reference to avoid circular import

    class Config:
        from_attributes = True

# Explicitly rebuild the model after all dependencies are resolved
SearchResponse.model_rebuild()