from dataclasses import asdict

from pydantic.dataclasses import dataclass


@dataclass
class LatLng:
    lat: str
    lng: str


@dataclass
class Address:
    street: str
    suite: str
    city: str
    zipcode: str
    geo: LatLng

    def to_json(self):
        return asdict(self)


@dataclass
class Company:
    name: str
    catchPhrase: str
    bs: str

    def to_json(self):
        return asdict(self)


@dataclass
class User:
    id: int
    name: str
    username: str
    email: str
    phone: str
    website: str
    address: Address | None = None
    company: Company | None = None

    def to_json(self):
        return asdict(self)
