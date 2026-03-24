from typing import Protocol


class ProductProtocol(Protocol):
    async def get_products(self): ...
