from litestar import Litestar
from strawberry.litestar import make_graphql_controller

from opentransit.data.fake_repository import (
    FakeTransitNetworkRepository,
    FakeTransitRouteRepository,
    FakeTransitStopRepository,
)
from opentransit.graphql.context import CustomContext
from opentransit.graphql.schema import schema


async def custom_context_getter() -> CustomContext:
    return CustomContext(
        transit_network_repository=FakeTransitNetworkRepository(),
        transit_route_repository=FakeTransitRouteRepository(),
        transit_stop_repository=FakeTransitStopRepository(),
    )


GraphQLController = make_graphql_controller(
    schema,
    path="/graphql",
    context_getter=custom_context_getter,
)

app = Litestar(route_handlers=[GraphQLController])
