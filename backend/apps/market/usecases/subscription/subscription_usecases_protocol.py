from typing import Protocol

from apps.market.entities.subscription import Subscription


class SubscriptionProtocol(Protocol):
    async def get_subscribitions(self) -> list[Subscription]: ...
