import logging

import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from fastapi.security import HTTPBearer
from motor.motor_asyncio import AsyncIOMotorClient

from api.v1 import user, movie
from core import get_settings
from db import mongo

settings = get_settings()
security = HTTPBearer()

app = FastAPI(
    title=settings.app.project_name,
    version="1.0.0",
    docs_url="/api/v1/docs",
    openapi_url="/api/v1/openapi.json",
    default_response_class=ORJSONResponse,
)


@app.on_event("startup")
async def startup():
    mongo_uri = "mongodb://{host}:{port}".format(
        host=settings.mongo.host,
        port=settings.mongo.port,
    )
    try:
        mongo.mongo = AsyncIOMotorClient(mongo_uri)
        logging.info('mongodb %s successfully connected', mongo_uri)
    except (ConnectionError, Exception) as e:
        logging.exception('Cannot connect to mongo %s', mongo_uri)


@app.on_event("shutdown")
async def shutdown():
    await mongo.mongo.close()
    logging.debug('mongodb successfully closed')


app.include_router(movie.router, prefix="/api/v1/movie", tags=["movie"])
app.include_router(user.router, prefix="/api/v1/user", tags=["user"])

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8008,
        log_config=settings.app.logging,
        log_level=logging.DEBUG,
        reload=True
    )
