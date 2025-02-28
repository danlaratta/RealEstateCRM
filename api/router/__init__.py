from fastapi import APIRouter
from api.router.routes.auth_route import router as auth_router

router = APIRouter()
router.include_router(auth_router)