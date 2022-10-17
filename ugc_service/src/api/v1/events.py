from http import HTTPStatus

from fastapi import APIRouter, HTTPException

from src.core import AVAILABLE_TOPICS
from src.kafka_ugc.producer import get_producer
from src.models.producer_models import EventModel, ProducerResponseModel

router = APIRouter()


@router.post('/send_event/{topic}', response_model=ProducerResponseModel)
async def send_event(event: EventModel, topic: str) -> ProducerResponseModel:
    if topic not in AVAILABLE_TOPICS:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='topic not available')
    producer = await get_producer()
    try:
        await producer.start()
        await producer.send_and_wait(topic, **event.dict())
    finally:
        await producer.stop()
    response = ProducerResponseModel(topic=topic, **event.dict())
    return response
