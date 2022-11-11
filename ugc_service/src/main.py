import asyncio
import json
import logging

import uvicorn
from aiokafka import AIOKafkaProducer
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from api.v1 import events
from core import get_settings
from kafka_ugc import producer

settings = get_settings()

app = FastAPI(
    title=settings.app.project_name,
    docs_url='/ugc_service/openapi',
    openapi_url='/ugc_service/openapi.json',
    default_response_class=ORJSONResponse,

)

loop = asyncio.get_event_loop()


@app.on_event('startup')
async def startup():
    try:
        producer.producer = AIOKafkaProducer(
            bootstrap_servers=settings.kafka_settings.host,
            loop=loop,
            key_serializer=lambda x: x.encode('utf-8'),
            value_serializer=lambda x: json.dumps(x).encode('utf-8'),
            compression_type="gzip"
        )
        await producer.producer.start()
        logging.info(f'producer successfully started')
    except (ConnectionError, Exception) as e:
        logging.exception('producer start failed with')


@app.on_event('shutdown')
async def shutdown():
    await producer.producer.stop()
    logging.debug('producer successfully stopped')


app.include_router(events.router, prefix='/ugc_service/v1/producer', tags=['producer'])

if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        reload=True,
        port=8000,
        log_config=settings.app.logging,
        log_level=logging.DEBUG,
    )
