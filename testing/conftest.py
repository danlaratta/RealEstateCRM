import pytest
from unittest.mock import MagicMock
from sqlalchemy.ext.asyncio import AsyncSession

@pytest.fixture
def mock_db_session():
    session = MagicMock(spec=AsyncSession)
    return session
