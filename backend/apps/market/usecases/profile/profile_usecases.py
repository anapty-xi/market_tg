from apps.market.entities.profile import Profile
from apps.market.usecases.profile.profile_usecases_protocol import ProfileProtocol


class Base:
    def __init__(self, inf: ProfileProtocol):
        self.inf = inf


class AddProfile(Base):
    async def execute(
        self, tg_id: int, username: str, phone_number: str
    ) -> None | Exception:
        try:
            user = Profile(tg_id=tg_id, username=username, phone_number=phone_number)
        except Exception:
            raise ValueError("data is invalid")

        await self.inf.add_user(user)


class HasPhoneNumber(Base):
    async def execute(self, tg_id: int, username: str) -> bool | Exception:
        try:
            user = Profile(tg_id=tg_id, username=username)
        except Exception:
            raise ValueError("data is invalid")

        return await self.inf.has_phone_number(user)
