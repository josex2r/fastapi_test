from dataclasses import asdict

from pydantic import BaseModel
from pydantic.dataclasses import dataclass


class LatLng(BaseModel):
    lat: str
    lng: str


class Address(BaseModel):
    street: str
    suite: str
    city: str
    zipcode: str
    geo: LatLng


class Company(BaseModel):
    name: str
    catchPhrase: str
    bs: str


class Person(BaseModel):
    id: int
    name: str
    username: str
    email: str
    phone: str
    website: str
    address: Address | None = None
    company: Company | None = None
