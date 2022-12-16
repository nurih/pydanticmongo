import pathlib
from pymongo import MongoClient
import uvicorn
from fastapi import FastAPI, HTTPException, status
from typing import Any, Dict, Union, AbstractSet, Mapping
from pydanticmongo import (
    MongoBaseModel,
    MongoIdField,
    StringAsObjectIdHandler,
    TransparentIdHandler,
)


IntStr = Union[int, str]
DictStrAny = Dict[str, Any]
MappingIntStrAny = Mapping[IntStr, Any]
AbstractSetIntStr = AbstractSet[IntStr]

ID_HANDLER = StringAsObjectIdHandler()

db = MongoClient("mongodb://localhost/test").get_default_database()


class Demo(MongoBaseModel):
    UserId: str | None = MongoIdField()  # A MongoIdField with default id_handler
    N: int | None = 123


class Customer(MongoBaseModel):
    Email: str = MongoIdField(
        id_handler=TransparentIdHandler(default_factory= lambda: "JUST DON'T")
    )  # A MongoIdField with specific id_handler
    Name: str = "bob"


api = FastAPI()


@api.get("/1")
async def d1():
    result = Demo(x=100)
    return result


@api.get("/2", response_model=Demo)
async def d2():
    result = Demo(x=200)
    return result


@api.get("/3", response_model=Demo)
async def d3():
    result = Demo(x=300)
    return result.dict()


@api.get("/4")
async def d4():
    result = Demo(x=400)
    return result.dict()


@api.get("/5")
async def d5():
    """Expect failure

    The dict from `mongo_doc()` has a native mongo `ObjectId` assigned to `_id`.
    mongo_doc returns a dict with _id set to ObjectId(...). FastAPI will try to jsonify directly and fails on the ObjectId() serialization.
    """
    result = Demo(x=500)
    return result.mongo_doc()


@api.get("/6", response_model=Demo)
async def d6():
    """Expect success
    `respons_model` tells FastAPI to create a `Demo` model from the raw dict, and that works.
    """
    result = Demo(x=600)
    return result.mongo_doc()


@api.post("/d0")
async def d0(demo: Demo):
    """MongoModel knows how to produce `mongo_doc`

    It uses the field we assigned as a Mongo id field, and the handler that knows what to do.
    """
    result = db.demo.insert_one(demo.mongo_doc())
    return {"ok": ID_HANDLER.to_model_type(result.inserted_id)}


@api.get("/7/{id}", response_model=Demo)
async def d7(id: str):
    """A `MongoIdHandler` knows how to encode / decode the _id field

    Here it is used directly
    """

    result = db.demo.find_one({"_id": ID_HANDLER.from_model_type(id)})
    if not result:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, detail=f"No document matches id {id}"
        )
    return result


@api.post("/customer")
async def create_customer(c: Customer):
    result = db.customer.insert_one(c.mongo_doc())
    return {"ok": ID_HANDLER.to_model_type(result.inserted_id)}


@api.get("/customer/{id}", response_model=Customer)
async def create_customer(id: str):
    result = db.customer.find_one(id)
    if not result:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, detail=f"No document matches id {id}"
        )
    return result


# Manual entry point
if __name__ == "__main__":
    """Entry point to activate uvicorn"""
    uvicorn.run(f"{pathlib.Path(__file__).stem}:api", reload=True)
