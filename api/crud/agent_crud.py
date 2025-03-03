from fastapi import HTTPException, status, Response
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import Optional
from api.schemas import AgentCreate, AgentUpdate
from ..crud.user_crud import get_user
from ..models import Agent, User


# Create Agent
async def create_agent(db: AsyncSession, user_id: int, agent: AgentCreate) -> Agent:
    # Get User who's creating/saving Agent
    user: User = await get_user(db, user_id)

    try:
        # Create Agent linking to User
        new_agent: Agent = Agent(**agent.model_dump(), user_id = user.id)

        # Save to database
        db.add(new_agent)
        await db.commit()
        await db.refresh(new_agent)
        return new_agent
    except IntegrityError:  # Handle unique constraint violations
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already exists")
    except SQLAlchemyError:
        await db.rollback()  # Ensure rollback on failure
        raise database_exception()  # Custom database error handling


# Get a single agent by ID
async def get_agent(db: AsyncSession, user_id: int, agent_id: int) -> Agent:
        # Query for the user's agent
        result = await db.execute(select(Agent).filter(Agent.id == agent_id, Agent.user_id == user_id))
        agent: Optional[Agent] = result.scalar_one_or_none()

        if agent is None:
            raise HTTPException(status_code=404, detail="Agent not found")

        if agent.user_id != user_id:
            raise HTTPException(status_code=403, detail="Access denied")

        return agent


# Get all agents
async def get_all_agents(db: AsyncSession, user_id: int) -> list[Agent]:
    result = await db.execute(select(Agent).filter(Agent.user_id == user_id))
    agents: Optional[list[Agent]] = list[Agent](result.scalars().all())
    return agents # returns empty list if no agents found


# Update Agent
async def update_agent(db: AsyncSession, user_id: int, agent_id: int, agent_update: AgentUpdate) -> Agent:
    # Get agent to update
    agent: Agent = await get_agent(db, user_id, agent_id)

    try:
        # Update the agent with updated_data
        for key, value in agent_update.model_dump(exclude_unset=True).items():
            setattr(agent, key, value)

        # Commit updates to the database
        await db.commit()
        await db.refresh(agent)
        return agent
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Duplicate entry detected")

    except SQLAlchemyError:
        await db.rollback()  # rollback db session prior to issue
        raise database_exception()


# Delete Agent
async def delete_agent(db: AsyncSession, user_id: int, agent_id: int) -> Response:
    # Get agent to delete
    agent: Agent = await get_agent(db, user_id, agent_id)

    try:
        # Delete the agent
        await db.delete(agent)
        await db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)  # Response signifies deletion
    except SQLAlchemyError :
        await db.rollback()  # rollback db session prior to issue
        raise database_exception()


# Custom Exception
def database_exception()-> HTTPException:
    return HTTPException (status_code= status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'Database Error Occurred')