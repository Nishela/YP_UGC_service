from typing import Dict

from .model_meta import ModelMeta
from .models_mixin import ProducerMixin

__all__ = (
    'EventModel',
)


class EventModel(ProducerMixin, metaclass=ModelMeta):
    def __init__(self, event_name: str, user_id: str, data: Dict[str, str]):
        self.event_name = event_name
        self.user_id = user_id
        self.data = data
