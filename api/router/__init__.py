from fastapi import APIRouter
from api.router.routes.user_routes import router as user_routes
from api.router.routes.auth_routes import router as auth_routes
from api.router.routes.agent_routes import router as agent_routes
from api.router.routes.search_category_routes import router as category_routes
from api.router.routes.property_search_routes import router as search_routes
from api.router.routes.listing_routes  import router as listing_routes
from api.router.routes.lead_routes  import router as lead_routes


router = APIRouter()
router.include_router(user_routes)
router.include_router(auth_routes)
router.include_router(agent_routes)
router.include_router(category_routes)
router.include_router(search_routes)
router.include_router(listing_routes)
router.include_router(lead_routes)