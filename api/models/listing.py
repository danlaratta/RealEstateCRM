from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from api.models import Base, Lead
from typing import Optional

class Listing(Base):
    # define table name
    __tablename__ = 'listings'

    # define table attributes/columns
    zpid: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    address: Mapped[str] = mapped_column(String(255), nullable=False)
    price: Mapped[int] = mapped_column(Integer, nullable=False)
    status_type: Mapped[str] = mapped_column(String(50), nullable=False)
    home_type: Mapped[str] = mapped_column(String(50), nullable=False, default='Houses')
    bedrooms: Mapped[int] = mapped_column(Integer, nullable=False)
    bathrooms: Mapped[int] = mapped_column(Integer, nullable=False)
    square_ft: Mapped[int] = mapped_column(Integer, nullable=False)
    days_on_market: Mapped[int] = mapped_column(Integer, nullable=False)
    # agent_id: Mapped[int] = mapped_column(Integer, ForeignKey('agents.id', ondelete='CASCADE'), nullable=False) # FK links to agents table

    # Relationships
    lead: Mapped[Optional['Lead']] = relationship('Lead', back_populates='listing', uselist=False) # One-to-One Relationship with Lead
#     agent: Mapped['Agent'] = relationship(back_populates='listings')
