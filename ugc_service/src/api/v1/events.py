from fastapi import APIRouter

from src.kafka_ugc.producer import get_producer
from src.models.producer_models import EventModel, ProducerResponseModel

router = APIRouter()


@router.post('/send_event/{topic}', response_model=ProducerResponseModel)
async def send_event(event: EventModel, topic: str) -> ProducerResponseModel:
    producer = await get_producer()
    try:
        await producer.start()
        await producer.send_and_wait(topic, **event.dict())
    finally:
        await producer.stop()
    response = ProducerResponseModel(topic=topic, **event.dict())
    return response
