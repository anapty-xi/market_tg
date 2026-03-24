from apps.market.entities.subscription import Subscription
from apps.market.usecases.subscription.subscription_usecases_protocol import (
    SubscriptionProtocol,
)


class Base:
    def __init__(self, inf: SubscriptionProtocol):
        self.inf = inf


class GetSubscriptions(Base):
    async def execute(self) -> list[Subscription]:
        return await self.inf.get_subscribitions()
