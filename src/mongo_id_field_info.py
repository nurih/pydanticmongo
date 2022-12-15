from typing import Any
from pydantic.fields import FieldInfo

from mongo_id_handler import StringAsObjectIdHandler


class MongoFieldInfo(FieldInfo):
    def __init__(self, default: Any = ...,  id_handler=StringAsObjectIdHandler(), **kwargs: Any) -> None:
        self.id_handler = id_handler
        kwargs['default_factory'] = id_handler.default_factory
        super().__init__(default, **kwargs)
