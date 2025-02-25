from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from api.models import Base
from datetime import datetime
from typing import TYPE_CHECKING

# Avoid circule import
if TYPE_CHECKING:
    from .agent import Agent

class Listing(Base):
    # define table name
    __tablename__ = 'listings'

    # define table attributes/columns
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    address: Mapped[str] = mapped_column(String(255), nullable=False)
    price: Mapped[int] = mapped_column(Integer, nullable=False)
    beds: Mapped[int] = mapped_column(Integer, nullable=False)
    baths: Mapped[int] = mapped_column(Integer, nullable=False)
    square_ft: Mapped[int] = mapped_column(Integer, nullable=False)
    days_on_market: Mapped[int] = mapped_column(Integer, nullable=False)
    status: Mapped[str] = mapped_column(String(100), nullable=False, default= 'New')
    interest_level: Mapped[str] = mapped_column(String(100), nullable=False)
    date_saved: Mapped[datetime] = mapped_column(default=datetime.now())

    # Relationships
    agent: Mapped['Agent'] = relationship(back_populates='listings')
