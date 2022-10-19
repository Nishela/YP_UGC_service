class ModelMeta(type):
    def __new__(cls, name, bases, dct):
        model_class = super().__new__(cls, name, bases, dct)
        model_class.producer = model_class.ProducerConfig.producer(model_class)
        return model_class
