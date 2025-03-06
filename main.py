from fastapi import FastAPI
from api.router import router
from external_api.external_api_service import ApiService
from api.schemas.propery_search_schema import SearchBase

# create instance of FastApi
app = FastAPI()

# add all routes to app
app.include_router(router)
