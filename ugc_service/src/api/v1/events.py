from http import HTTPStatus
from typing import Any

from fastapi import APIRouter, HTTPException

from api.v1.schemas import EventSchema
from core import get_settings
from models import EventModel

settings = get_settings()
router = APIRouter()


@router.post('/send_event', response_model=HTTPStatus)
async def send_event(event: EventSchema) -> Any:
    if not (topic := settings.topics.get(event.event_name)):
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='event_name not found')
    event_instance = EventModel(**event.dict())
    await event_instance.producer.async_post_event(event_instance, topic)
    return HTTPStatus.CREATED
