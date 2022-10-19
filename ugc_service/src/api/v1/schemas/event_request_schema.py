from pydantic import BaseModel

__all__ = (
    'EventSchema',
)


class EventDataSchema(BaseModel):
    movie_id: str
    value: str


class EventSchema(BaseModel):
    event_name: str
    user_id: str
    data: EventDataSchema
