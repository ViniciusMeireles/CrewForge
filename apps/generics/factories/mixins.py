import factory


class ModelFactoryMixin:
    """
    A mixin class that provides a factory method for creating instances of a model.
    """

    id = factory.Faker('id')
    is_active = True
