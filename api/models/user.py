from typing import TYPE_CHECKING
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from api.models import Base

# Avoid circule import
if TYPE_CHECKING:
    from .agent import Agent
    from .property_search import PropertySearch
    from .search_category import SearchCategory
    from .lead import Lead

class User(Base):
    # define table name
    __tablename__ = 'users'

    # define table attributes/columns
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    phone: Mapped[str] = mapped_column(String(10), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)

    # Relationships
    agents: Mapped[list['Agent']] = relationship(lazy='selectin') # one to many with Agent
    leads: Mapped[list['Lead']] = relationship(lazy='selectin') # one to many with Lead
    searches: Mapped[list['PropertySearch']] = relationship(lazy='selectin') # one to many with PropertySearch
    categories: Mapped[list['SearchCategory']] = relationship(lazy='selectin') # one to many with SearchCategory