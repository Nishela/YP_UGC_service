import logging

import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from src.core.logger import LOGGING

app = FastAPI(
    title='...',
    docs_url='/ugc_service/openapi',
    openapi_url='/ugc_service/openapi',
    default_response_class=ORJSONResponse,
)


@app.on_event('startup')
async def startup():
    ...


@app.on_event('shutdown')
async def shutdown():
    ...


if __name__ == '__main__':
    # only for develop (production use nginx + gunicorn server)
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        reload=True,
        port=8000,
        log_config=LOGGING,
        log_level=logging.DEBUG,
    )
