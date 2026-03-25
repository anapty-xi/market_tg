from apps.market.entities.profile import Profile
from apps.market.models import Profile as DBProfile
from apps.market.usecases.profile.profile_usecases_protocol import ProfileProtocol


class ProfileDBGW(ProfileProtocol):
    async def add_user(self, user: Profile) -> None:
        user_dict = user.model_dump()
        await DBProfile.objects.acreate(**user_dict)

    async def has_phone_number(self, user: Profile) -> bool:
        try:
            await DBProfile.objects.aget(tg_id=user.tg_id, username=user.username)
            return True
        except Exception:
            return False
