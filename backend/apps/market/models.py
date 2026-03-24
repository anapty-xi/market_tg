from django.db import models


class Profile(models.Model):
    tg_id = models.BigIntegerField(primary_key=True)
    username = models.CharField(max_length=128, null=True, blank=True)
    phone_number = models.CharField(max_length=16, null=True, blank=True)

    def __str__(self):
        return f"{self.username} ({self.tg_id})"


class Subscription(models.Model):
    name = models.CharField(max_length=64)
    channel_id = models.CharField(
        max_length=128, help_text="ID канала для проверки ботом"
    )
    link = models.URLField(max_length=128)


class Category(models.Model):
    name = models.CharField(max_length=128)
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="subcategories",
    )

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="products"
    )

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="images"
    )
    image = models.ImageField(upload_to="products/")


class CartItem(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="cart")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    @property
    def total_price(self):
        return self.product.price * self.quantity


class Order(models.Model):
    class Status(models.TextChoices):
        PAID = "paid", "Оплачен"
        UNPAID = "unpaid", "Неоплачен"
        ON_THE_WAY = "on_the_way", "В пути"
        DONE = "done", "Выполнен"

    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.UNPAID
    )
    client = models.ForeignKey(Profile, on_delete=models.CASCADE)
    address = models.TextField()
    client_full_name = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    price_at_purchase = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)


class FAQ(models.Model):
    question = models.CharField(max_length=255)
    answer = models.TextField()
    active = models.BooleanField(default=True)
