from __future__ import annotations

from typing import Self, cast

import strawberry

from opentransit.graphql.context import CustomInfo
from opentransit.model.id import ID
from opentransit.model.misc import Location as LocationModel
from opentransit.model.transit import TransitNetwork as TransitNetworkModel
from opentransit.model.transit import TransitRoute as TransitRouteModel
from opentransit.model.transit import TransitStop as TransitStopModel


def gql_id(id: ID) -> strawberry.ID:
    return cast(strawberry.ID, id)


def model_id(id: strawberry.ID) -> ID:
    return cast(ID, id)


# ======================================================================================


@strawberry.type
class TransitNetwork:
    id: strawberry.ID
    name: str

    @strawberry.field
    def routes(self, info: CustomInfo) -> list[TransitRoute]:
        routes = info.context.transit_route_repository.get_all_for_network(
            model_id(self.id)
        )
        return list(map(TransitRoute.from_model, routes))

    @strawberry.field
    def stops(self, info: CustomInfo) -> list[TransitStop]:
        stops = info.context.transit_stop_repository.get_all_for_network(
            model_id(self.id)
        )
        return list(map(TransitStop.from_model, stops))

    @classmethod
    def from_model(cls, model: TransitNetworkModel) -> Self:
        return cls(
            id=gql_id(model.id),
            name=model.name,
        )


@strawberry.type
class TransitRoute:
    id: strawberry.ID
    number: str

    @classmethod
    def from_model(cls, model: TransitRouteModel) -> Self:
        return cls(id=gql_id(model.id), number=model.number)


@strawberry.type
class TransitStop:
    id: strawberry.ID
    name: str
    location: Location

    @classmethod
    def from_model(cls, model: TransitStopModel) -> Self:
        return cls(
            id=gql_id(model.id),
            name=model.name,
            location=Location.from_model(model.location),
        )


@strawberry.type
class Location:
    lat: str
    lon: str

    @classmethod
    def from_model(cls, model: LocationModel) -> Self:
        return cls(lat=model.lat, lon=model.lon)


# ======================================================================================


@strawberry.type
class Query:
    @strawberry.field
    def networks(self, info: CustomInfo) -> list[TransitNetwork]:
        models = info.context.transit_network_repository.get_all()
        return list(map(TransitNetwork.from_model, models))


schema = strawberry.Schema(query=Query)
