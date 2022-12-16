
from pydantic import BaseModel
from typing import Any, Callable, Dict, Union, AbstractSet, Mapping

from .idfield import MongoFieldInfo

IntStr = Union[int, str]
DictStrAny = Dict[str, Any]
MappingIntStrAny = Mapping[IntStr, Any]
AbstractSetIntStr = AbstractSet[IntStr]
NoArgAnyCallable = Callable[[], Any]


class MongoBaseModel(BaseModel):
    _id_field = None

    def __init__(__pydantic_self__, **data: Any) -> None:
        """ Create a new MongoBaseModel by parsing and validating input data from keyword arguments.
        MongoBaseModel expects exactly one field created using ``MongoIdField``.
        Raises ValidationError if the input data cannot be parsed to form a valid model.
        Raises AssertionError if the descendant class does not have exactly one ``MongoIdField`` used on one field.
        """

        # No work if field memoized
        if not MongoBaseModel._id_field:
            mongo_fields = [f for f in __pydantic_self__.__fields__.values(
            ) if isinstance(f.field_info, MongoFieldInfo)]

            if len(mongo_fields) != 1:
                raise AssertionError(
                    f'MongoBaseModel must have exactly one MongoIdField. Found {len(mongo_fields)}')

            id_field = mongo_fields.pop()

            MongoBaseModel._id_field = id_field

        # If incoming data is coming in as a mongo document with an _id, slam the nominal field with its value
        # This is the case where a serializer tries to take a dict / object from mongo document, and populate
        # the model. Since _id is not a nominal field, it needs to be converted into its nominal counterpart.
        mongo_native_value = data.get('_id')
        if mongo_native_value:
            data[MongoBaseModel._id_field.name] = MongoBaseModel._id_field.field_info.id_handler.to_model_type(
                data.pop('_id'))

        super().__init__(**data)

    def mongo_doc(
            self, *, include: Union['AbstractSetIntStr', 'MappingIntStrAny'] = None, exclude: Union['AbstractSetIntStr', 'MappingIntStrAny'] = None, by_alias: bool = False, skip_defaults: bool = None, exclude_unset: bool = False, exclude_defaults: bool = False, exclude_none: bool = False) -> 'DictStrAny':
        """ Generate a dictionary suitable for a MongoDB document, with the `_id` field populated 
        from the pydantic field that was assigned a ``MongoIdField``
        """
        result = super().dict(
            include=include, exclude=exclude, by_alias=by_alias, skip_defaults=skip_defaults,
            exclude_unset=exclude_unset, exclude_defaults=exclude_defaults, exclude_none=exclude_none)

        id_field = MongoBaseModel._id_field
        result['_id'] = id_field.field_info.id_handler.from_model_type(
            result.pop(id_field.name))

        return result
