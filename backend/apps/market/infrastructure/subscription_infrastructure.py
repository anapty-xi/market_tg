from apps.market.entities.subscription import Subscription
from apps.market.models import Subscription as DBSub
from apps.market.usecases.subscription.subscription_usecases_protocol import (
    SubscriptionProtocol,
)


class SubscriptionDVGW(SubscriptionProtocol):
    async def get_subscribitions(self) -> list[Subscription]:
        orm_subs = DBSub.objects.all()
        return [Subscription.model_validate(sub) async for sub in orm_subs]
