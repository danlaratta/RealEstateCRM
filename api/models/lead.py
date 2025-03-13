from sqlalchemy import Integer, String, ForeignKey, TIMESTAMP, UniqueConstraint
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
    date_saved: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), nullable=False, default=datetime.now(UTC))
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False) # FK links to users table
    zpid: Mapped[int] = mapped_column(Integer, ForeignKey('listings.zpid', ondelete='CASCADE'), nullable=False) # FK links to listing table

    # Relationship (lazy='joined' Ensures it eagerly loads within session context)
    listing: Mapped['Listing'] = relationship('Listing', back_populates='lead', uselist=False, cascade='all, delete', lazy='joined')

    #  Ensures each listing_id in the Lead table is unique, meaning a listing can have at most one associated lead (one-to-one relationship)
    __table_args__ = (UniqueConstraint('zpid', name='unique_lead_listing'),)
