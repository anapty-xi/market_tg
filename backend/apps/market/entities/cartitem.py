from entities.product import Product
from entities.profile import Profile
from pydantic import BaseModel, ConfigDict, Field, computed_field


class CartItem(BaseModel):
    conf = ConfigDict(from_attributes=True)

    id: int
    user: Profile
    product: Product
    quantity: int = Field(gt=0)

    @computed_field
    @property
    def total_price(self):
        return self.quantity * self.product.price
