from typing import Any

from pydantic import BaseModel

__all__ = (
    'EventModel',
    'ProducerResponseModel',
)


class EventModel(BaseModel):
    key: str
    value: Any


class ProducerResponseModel(BaseModel):
    key: str
    value: Any
    topic: str
