from dataclasses import dataclass

from opentransit.model.id import ID
from opentransit.model.misc import Location


@dataclass
class TransitNetwork:
    id: ID
    name: str


@dataclass
class TransitRoute:
    id: ID
    number: str
    network_id: ID


@dataclass
class TransitStop:
    id: ID
    name: str
    location: Location
    network_id: ID
