from ugc_service.src.models.model_producer import ModelProducer

__all__ = (
    'ProducerMixin',
)


class ProducerMixin:
    class ProducerConfig:
        producer = ModelProducer
