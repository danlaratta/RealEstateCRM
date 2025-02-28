from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING
from api.models import Base

# Avoid circule import
if TYPE_CHECKING:
    from .listing import Listing

class Agent(Base):
    # define table name
    __tablename__ = 'agents'

    # define table attributes/columns
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    phone: Mapped[str] = mapped_column(String(10), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False) # FK links to users table

    # Relationships
    listings: Mapped[list['Listing']] = relationship(back_populates='agent', lazy='selectin')

