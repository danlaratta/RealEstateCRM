from fastapi import HTTPException, status, Response
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import Optional
from api.schemas import AgentCreate, AgentUpdate
from ..crud.user_crud import get_user
from ..models import Agent, User
from ..router.exceptions import database_exception

# Create Agent
async def create_agent(db: AsyncSession, user_id: int, agent: AgentCreate) -> Agent:
    # Get User who's creating/saving Agent
    user: User = await get_user(db, user_id)

    # Create Agent linking to User
    new_agent: Agent = Agent(**agent.model_dump(), user_id=user.id)

    try:
        # Save to database
        db.add(new_agent)
        await db.commit()
        await db.refresh(new_agent)
        return new_agent
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Agent already exists")
    except SQLAlchemyError as e:
        await db.rollback()
        raise database_exception(e)


# Get a single agent by ID
async def get_agent(db: AsyncSession, user_id: int, agent_id: int) -> Agent:
        # Query for specific agent
        result = await db.execute(select(Agent).where(Agent.id == agent_id, Agent.user_id == user_id))
        agent: Optional[Agent] = result.scalar_one_or_none()

        if agent is None:
            raise HTTPException(status_code=404, detail="Agent not found")

        return agent


# Get all agents
async def get_all_agents(db: AsyncSession, user_id: int) -> list[Agent]:
    # Query for all agents
    result = await db.execute(select(Agent).where(Agent.user_id == user_id))
    agents: Optional[list[Agent]] = list[Agent](result.scalars().all())

    if agents is None:
        raise HTTPException(status_code=404, detail="No Agents found")

    return agents # returns empty list if no agents are found


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
    except SQLAlchemyError as e:
        await db.rollback()
        raise database_exception(e)


# Delete Agent
async def delete_agent(db: AsyncSession, user_id: int, agent_id: int) -> Response:
    # Get agent to delete
    agent: Agent = await get_agent(db, user_id, agent_id)

    try:
        # Delete the agent
        await db.delete(agent)
        await db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)  # Response signifies deletion
    except SQLAlchemyError as e:
        await db.rollback()
        raise database_exception(e)


