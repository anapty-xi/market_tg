class NotFound(Exception):
    pass


class UserNotExists(NotFound):
    pass


class ProductNotExists(NotFound):
    pass


class CartNotExists(NotFound):
    pass


class CartItemNotExists(NotFound):
    pass


class OrderNotExists(NotFound):
    pass


class InvalidStatus(Exception):
    pass
