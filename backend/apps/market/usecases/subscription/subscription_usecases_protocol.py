from typing import Protocol


class SubscriptionProtocol(Protocol):
    async def get_subscribitions(self) -> list[dict[str, str | int]]: ...
