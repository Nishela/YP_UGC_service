import asyncio
import json
import logging

import uvicorn
from aiokafka import AIOKafkaProducer
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from core import KAFKA_PRODUCER_CONFIG
from src.api.v1 import events
from src.core.logger import LOGGING
from src.kafka_ugc import producer

app = FastAPI(
    title='...',
    docs_url='/ugc_service/openapi',
    openapi_url='/ugc_service/openapi.json',
    default_response_class=ORJSONResponse,
)

loop = asyncio.get_event_loop()


@app.on_event('startup')
async def startup():
    producer.producer = AIOKafkaProducer(
        bootstrap_servers=KAFKA_PRODUCER_CONFIG.KAFKA_BOOTSTRAP_SERVERS,
        loop=loop,
        key_serializer=lambda x: x.encode('utf-8'),
        value_serializer=lambda x: json.dumps(x).encode('utf-8'),
    )


@app.on_event('shutdown')
async def shutdown():
    ...


app.include_router(events.router, prefix='/ugc_service/v1/producer', tags=['producer'])

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
