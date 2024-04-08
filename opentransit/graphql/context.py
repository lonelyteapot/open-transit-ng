import strawberry
from strawberry.litestar import BaseContext

from opentransit.data.repository import (
    TransitNetworkRepository,
    TransitRouteRepository,
    TransitStopRepository,
)


class CustomContext(BaseContext):
    transit_network_repository: TransitNetworkRepository
    transit_route_repository: TransitRouteRepository
    transit_stop_repository: TransitStopRepository


CustomInfo = strawberry.Info[CustomContext, None]
