from typing import Protocol


class SettingsProtocol(Protocol):
    async def get_admin_group_id(self) -> int: ...
