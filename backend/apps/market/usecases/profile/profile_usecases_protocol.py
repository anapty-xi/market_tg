from typing import Protocol

from apps.market.entities.profile import Profile


class ProfileProtocol(Protocol):
    async def add_user(self, user: Profile) -> None: ...
    async def has_phone_number(self, user: Profile) -> bool: ...
