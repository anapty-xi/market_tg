from decimal import Decimal

from apps.market.entities.product import Product
from apps.market.entities.profile import Profile
from pydantic import BaseModel, ConfigDict, Field, computed_field


class CartItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user: Profile
    product: Product
    quantity: int = Field(gt=0)

    @computed_field
    @property
    def total_price(self) -> Decimal:
        return self.quantity * self.product.price
