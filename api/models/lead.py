from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from api.models import Base
from datetime import datetime, UTC
from typing import TYPE_CHECKING

# Avoid circule import
if TYPE_CHECKING:
    from .listing import Listing

class Lead(Base):
    # define table name
    __tablename__ = 'leads'

    # define table attributes/columns
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    status: Mapped[str] = mapped_column(String(100), nullable=False, default= 'New')
    interest_level: Mapped[str] = mapped_column(String(100), nullable=False)
    date_saved: Mapped[datetime] = mapped_column(default=datetime.now(UTC))
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False) # FK links to users table
    listing_id: Mapped[int] = mapped_column(Integer, ForeignKey('listings.zpid', ondelete='CASCADE'), nullable=False) # FK links to listing table

    # Relationships
    listing: Mapped['Listing'] = relationship(lazy='selectin')


