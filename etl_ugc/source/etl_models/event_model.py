from pydantic import BaseModel

__all__ = (
    'EventModel',
)


class EventModel(BaseModel):
    event_name: str
    movie_id: str
    user_id: str
    event_data: str
    timestamp: str
