from __future__ import annotations

from abc import ABC, abstractmethod

from opentransit.model.id import ID
from opentransit.model.transit import TransitNetwork, TransitRoute, TransitStop


class TransitNetworkRepository(ABC):
    @abstractmethod
    def get_all(self) -> list[TransitNetwork]:
        raise NotImplementedError


class TransitRouteRepository(ABC):
    @abstractmethod
    def get_all_for_network(self, network_id: ID) -> list[TransitRoute]:
        raise NotImplementedError


class TransitStopRepository(ABC):
    @abstractmethod
    def get_all_for_network(self, network_id: ID) -> list[TransitStop]:
        raise NotImplementedError
