from apps.market.entities.subscription import Subscription
from apps.market.usecases.subscription.subscription_usecases_protocol import (
    SubscriptionProtocol,
)


class Base:
    def __init__(self, inf: SubscriptionProtocol):
        self.inf = inf


class GetSubscriptions(Base):
    async def execute(self) -> list[Subscription]:
        list_subs = await self.inf.get_subscribitions()
        return [Subscription(**sub) for sub in list_subs]
