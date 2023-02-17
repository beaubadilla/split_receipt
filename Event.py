from dataclasses import dataclass


@dataclass
class Event:
    name: str
    phone_number: str = None
    street_address: str = None
    zipcode: str = None
    city: str = None
    state: str = None
    country: str = None
    website: str = None
