from pydantic import BaseModel

__all__ = (
    'EventModel',
)


class EventDataModel(BaseModel):
    movie_id: str
    value: str


class EventModel(BaseModel):
    event_name: str
    user_id: str
    data: EventDataModel
