from typing import Any

from pydantic import BaseModel

# TODO: в зависимости от того, какую модель определит Серега
#  -> изменить эту модель
#  либо же импортировать модель напрямую из UGC сервиса


class EventModel(BaseModel):
    key: str
    value: Any