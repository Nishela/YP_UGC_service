from pydantic import BaseModel

__all__ = (
    'EventModel',
    'ProducerResponseModel',
)


class EventModel(BaseModel):
    key: str
    value: str
    timestamp: float = 0
    headers: dict = {}


class ProducerResponseModel(BaseModel):
    key: str
    value: str
    timestamp: float = 0
    headers: dict = {}
    topic: str
