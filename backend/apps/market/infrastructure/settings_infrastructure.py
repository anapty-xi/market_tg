from apps.market.models import GlobalSettings
from apps.market.usecases.settings.settings_usecases_protocol import SettingsProtocol


class SettingsDBGW(SettingsProtocol):
    async def get_admin_group_id(self) -> int:
        ids = GlobalSettings.objects.all().order_by("-id")
        return [id async for id in ids][0].admin_tg_id
