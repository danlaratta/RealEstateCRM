from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from api.models import Base
from typing import TYPE_CHECKING

# Avoid circule import
if TYPE_CHECKING:
    from .search_category import SearchCategory

class PropertySearch(Base):
    # define table name
    __tablename__ = 'property_searches'

    # define table attributes/columns
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    location: Mapped[str] = mapped_column(String(255), nullable=False)
    status_type: Mapped[str] = mapped_column(String(50), nullable=False, default='ForSale')
    home_type: Mapped[str] = mapped_column(String(50), nullable=False, default='Houses')
    price_min: Mapped[int] = mapped_column(Integer, nullable=False)
    price_max: Mapped[int] = mapped_column(Integer, nullable=False)
    beds_min: Mapped[int] = mapped_column(Integer, nullable=False)
    beds_max: Mapped[int] = mapped_column(Integer, nullable=False)
    baths_min: Mapped[int] = mapped_column(Integer, nullable=False)
    baths_max: Mapped[int] = mapped_column(Integer, nullable=False)
    square_ft_min: Mapped[int] = mapped_column(Integer, nullable=False)
    square_ft_max: Mapped[int] = mapped_column(Integer, nullable=False)
    category_id: Mapped[int] = mapped_column(Integer, ForeignKey('search_categories.id', ondelete='CASCADE'), nullable=False) # FK links to search_categories table
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id', ondelete='CASCADE'),nullable=False)  # FK links to users table

    # Relationships
    category: Mapped['SearchCategory'] = relationship(back_populates='searches') # many to one to SearchCategory