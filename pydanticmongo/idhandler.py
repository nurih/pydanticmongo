from bson import ObjectId

from typing import Any, Callable, Generic, TypeVar

M = TypeVar('M')
D = TypeVar('D')


class MongoIdHandler(Generic[M, D]):
    def __init__(self,
                 default_factory: Callable[[], M],
                 to_model_type: Callable[[D], M],
                 from_model_type: Callable[[M], D],
                 ) -> None:
        """ 
        Handles marshaling an id between the model stated type to the 'mongo' storage type.
        The 'mongo' type is actually some python type, which pymongo will then convert according to its own
        codec conventions.
        """
        self.default_factory = default_factory
        self.to_model_type = to_model_type
        self.from_model_type = from_model_type


class TransparentIdHandler(MongoIdHandler):
    def __init__(self, default_factory: Callable[[], Any]) -> None:
        super().__init__(default_factory, lambda d: d, lambda m: m)


class StringAsObjectIdHandler(MongoIdHandler):
    def __init__(self) -> None:
        """
        :param default_factory: A no-arguments callable that creates a new [Tmodel] value if none is supplied
        :param to_model_type: A [Tmodel] argument callable that converts the type from the one used in the document storage to the one the model expects
        :param from_model_type: A [Tdoc] the type from the one used the model exposes to the one the document should store
        """
        super().__init__(
            default_factory=lambda: str(ObjectId()),
            to_model_type=lambda oid: str(oid),
            from_model_type=lambda s: ObjectId(s)
        )
