from src.models.model_meta import ModelMeta
from src.models.models_mixin import ProducerMixin

__all__ = (
    'EventModel',
)


class EventModel(ProducerMixin, metaclass=ModelMeta):
    def __init__(self, event_name: str, user_id: str, data: dict):
        self.event_name = event_name
        self.user_id = user_id
        self.data = data


class ProducerResponseModel:
    ...
