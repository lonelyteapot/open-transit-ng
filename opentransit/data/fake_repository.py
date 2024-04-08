import faker
from faker.providers import address, geo

from opentransit.data.repository import (
    TransitNetworkRepository,
    TransitRouteRepository,
    TransitStopRepository,
)
from opentransit.model.id import ID
from opentransit.model.misc import Location
from opentransit.model.transit import TransitNetwork, TransitRoute, TransitStop

fake = faker.Faker()
fake.add_provider(geo)
fake.add_provider(address)


class FakeTransitNetworkRepository(TransitNetworkRepository):
    def get_all(self) -> list[TransitNetwork]:
        return [
            TransitNetwork(
                id=ID.generate_random(),
                name=fake.city(),
            )
            for _ in range(5)
        ]


class FakeTransitRouteRepository(TransitRouteRepository):
    def get_all_for_network(self, network_id: ID) -> list[TransitRoute]:
        return [
            TransitRoute(
                id=ID.generate_random(),
                number=fake.random_int(min=1, max=100),
                network_id=network_id,
            )
            for _ in range(fake.random_int(min=2, max=10))
        ]


class FakeTransitStopRepository(TransitStopRepository):
    def get_all_for_network(self, network_id: ID) -> list[TransitStop]:
        return [
            TransitStop(
                id=ID.generate_random(),
                name=fake.street_name(),
                location=Location(
                    lat=fake.latitude(),
                    lon=fake.longitude(),
                ),
                network_id=network_id,
            )
            for _ in range(fake.random_int(min=2, max=10))
        ]
