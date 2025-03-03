from fastapi import APIRouter, Depends, Response
from api.crud.agent_crud import create_agent, get_agent, get_all_agents, update_agent, delete_agent
from api.schemas.agent_schema import AgentResponse, AgentUpdate, AgentCreate
from sqlalchemy.ext.asyncio import AsyncSession
from api.database.database import get_db
from api.models.user import User
from api.models.agent import Agent
from ..services.auth_services import get_authenticated_user


# Define auth route
router = APIRouter(prefix='/agents')

# Create Agent
@router.post('/', response_model=AgentResponse, status_code=201)
async def create_agent_route(agent: AgentCreate, authenticated_user: User = Depends(get_authenticated_user), db: AsyncSession = Depends(get_db)) -> AgentResponse:
     new_agent: Agent = await create_agent(db, authenticated_user.id, agent)
     return AgentResponse.model_validate(new_agent)


# Get Agent
@router.get('/{agent_id}', response_model=AgentResponse, status_code=200)
async def get_agent_route(agent_id: int, authenticated_user: User = Depends(get_authenticated_user), db: AsyncSession = Depends(get_db)) -> AgentResponse:
    agent: Agent = await get_agent(db, authenticated_user.id, agent_id)
    return AgentResponse.model_validate(agent)


# Get Agents
@router.get('/', response_model=list[AgentResponse], status_code=200)
async def get_all_agents_route(authenticated_user: User = Depends(get_authenticated_user), db: AsyncSession = Depends(get_db)) -> list[AgentResponse]:
    agents: list[Agent] = await get_all_agents(db, authenticated_user.id)
    return [AgentResponse.model_validate(agent) for agent in agents]


# Update Agent
@router.put('/{agent_id}', response_model=AgentUpdate, status_code=200)
async def update_agent_route(agent_id: int, agent_update: AgentUpdate, authenticated_user: User = Depends(get_authenticated_user), db: AsyncSession = Depends(get_db)) -> AgentResponse:
    updated_agent: Agent = await update_agent(db, authenticated_user.id, agent_id, agent_update)
    return AgentResponse.model_validate(updated_agent)


# Delete Agent
@router.delete('/{agent_id}', status_code=204)
async def delete_agent_route(agent_id: int, authenticated_user: User = Depends(get_authenticated_user), db: AsyncSession = Depends(get_db)) -> Response:
    return await delete_agent(db, authenticated_user.id, agent_id)

