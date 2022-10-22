from http import HTTPStatus
from typing import Any

from fastapi import APIRouter, HTTPException

from ugc_service.src.api.v1.schemas import EventSchema
from ugc_service.src.core import AVAILABLE_TOPICS
from ugc_service.src.models import EventModel

router = APIRouter()


@router.post('/send_event', response_model=Any)
async def send_event(event: EventSchema) -> Any:
    if not (topic := AVAILABLE_TOPICS.get(event.event_name)):
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='event_name not found')
    event_instance = EventModel(**event.dict())
    await event_instance.producer.async_post_event(event_instance, topic)
    return {"status": 200}  # подумать нужен ли ответ вообще
