from apps.market.usecases.settings.settings_usecases_protocol import SettingsProtocol


class Base:
    def __init__(self, inf: SettingsProtocol):
        self.inf = inf


class GetAdminGroupId(Base):
    async def execute(self) -> int:
        return await self.inf.get_admin_group_id()
