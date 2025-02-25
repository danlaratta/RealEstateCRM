
from dotenv import load_dotenv
import os

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')

# establish asynchronous connection to a database (connects session to database)
engine = create_async_engine(DATABASE_URL, echo=True)

# Creates a factory for generating new asynchronous database sessions (session = the actual communitcation to DB like querying and committing)
AsyncSessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)

# Dependency to get the DB sessions
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

