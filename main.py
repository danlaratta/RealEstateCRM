from fastapi import FastAPI
from api.routes import router

# create instance of FastApi
app = FastAPI()

# add all routes to app
app.include_router(router)
