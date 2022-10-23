from ..model_producer import ModelProducer

__all__ = (
    'ProducerMixin',
)


class ProducerMixin:
    class ProducerConfig:
        producer = ModelProducer
