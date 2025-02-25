from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from api.models import Base
from typing import TYPE_CHECKING

# Avoid circule import
if TYPE_CHECKING:
    from .property_search import PropertySearch


class SearchCategory(Base):
    # define table name
    __tablename__ = 'search_categories'

    # define table attributes/columns
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)  # FK links to users table

    # Relationships
    searches: Mapped[list['PropertySearch']] = relationship(back_populates='category', lazy='selectin')  # one to many with ProperySearch