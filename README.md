# `pydanticmongo`

Things to make `pydantic` play nicer with MongoDB.

Current `pydantic` does not allow for a model to have an field named with an unserscore as the first character. MongoDB documents must support an `_id` field.

Inheriting `MongoBaseModel` instead of pydantic's `BaseModel` lets you handle this with less boilerplate code.

## How?

Given a model

```python
class MyModelOne(MongoBaseModel):
    UserId: str | None = MongoIdField()
    N: int | None = 123
# Or

class MyModelTwo(MongoBaseModel):
    Email: str = MongoIdField(id_handler=StringAsObjectIdHandler())
    Name: str = 'bob'
```

Writing to Mongo would be something along the lines of:

```python
def create_one(self, model_instance: MongoBaseModel) -> dict:
        doc = model_instance.mongo_doc()
        self.my_collection.insert_one(doc)
        return doc
```

Reading from Mongo would be someting along the lines of:

```python
def get_by_id(self, id: Any, id_handler: MongoIdHandler):
        target_value = id_handler.from_model_type(id) if self.id_handler else id
        return self.get_by_filter({"_id": target_value})
```


