from fastapi import APIRouter
from api.router.routes.user_route import router as user_route
from api.router.routes.auth_route import router as auth_route
from api.router.routes.agent_route import router as agent_route


router = APIRouter()
router.include_router(user_route)
router.include_router(auth_route)
router.include_router(agent_route)