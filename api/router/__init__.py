from fastapi import APIRouter
from api.router.routes.auth_route import router as auth_router
from api.router.routes.user_route import router as user_router

router = APIRouter()
router.include_router(auth_router)
router.include_router(user_router)