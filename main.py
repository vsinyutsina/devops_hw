from fastapi import FastAPI
from typing import Union
from pydantic import BaseModel
from enum import Enum
from fastapi import HTTPException
from collections import defaultdict


class Timestamp(BaseModel):
    id: int
    timestamp: int


class DogType(str, Enum):
    terrier = 'terrier'
    bulldog = 'bulldog'
    dalmatian = 'dalmatian'


class Dog(BaseModel):
    name: str
    pk: Union[int, None] = None
    kind: DogType


dogs_kind = defaultdict(list)
dogs_pk = dict()
app = FastAPI()


@app.get('/')
async def root():
    return {}


@app.post('/post')
async def get_post():

    timestamp = Timestamp(id=0, timestamp=0)
    return timestamp


@app.get('/dog')
async def get_dogs(kind: Union[DogType, None] = None):
    
    if kind is None:
        d = dict(dogs_kind)
        return [dog for v in d.values() for dog in v]
    
    dogs = dogs_kind[kind]
    return dogs


@app.post('/dog')
async def create_dog(dog: Dog):

    dog_id = len(dogs_pk)
    dog_kind = dog.kind
    new_dog = Dog(name=dog.name, kind=dog.kind, pk=dog_id)
    dogs_pk[dog_id] = new_dog
    dogs_kind[dog_kind].append(new_dog)

    return new_dog


@app.get('/dog/{pk}')
async def get_dog_by_pk(pk: int):

    id = pk
    if id not in dogs_pk.keys():
        raise HTTPException(status_code=404)
    dog = dogs_pk[id]
    return dog


@app.patch('/dog/{pk}')
async def update_dog(pk: int, dog: Dog):

    if pk >= len(dogs_pk):
        raise HTTPException(status_code=404)

    dog_kind = dog.kind
    dogs = dogs_kind[dog_kind]
    ind_replace = None

    for i, d in enumerate(dogs):
        if d == dog:
            ind_replace = i

    dog.pk = pk
    dogs_pk[pk] = dog

    if ind_replace is None:
        dogs_kind[dog_kind].append(dog)
    else:
        dogs_kind[dog_kind][ind_replace] = dog

    return dog
