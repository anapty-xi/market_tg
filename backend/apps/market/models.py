import json

from apps.market.tasks import execute_newsletter_mailing
from django.conf import settings
from django.db import models


class Profile(models.Model):
    tg_id = models.BigIntegerField(primary_key=True)
    username = models.CharField(max_length=128, null=True, blank=True)
    phone_number = models.CharField(max_length=16, null=True, blank=True)
    is_admin = models.BooleanField(default=False)

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

    # async def asave(self, *args, **kwargs):
    #     r = settings.REDIS_OBJ
    #     if self.pk:
    #         order = await Order.objects.select_related("client").aget(pk=self.pk)
    #         old_status = order.status
    #         if old_status != self.status:
    #             payload = {
    #                 "tg_id": self.client_id,
    #                 "order_id": self.pk,
    #                 "new_status": self.status,
    #             }
    #             await r.lpush("order_status_changed", json.dumps(payload))

    #     return await super().asave(*args, **kwargs)

    def save(self, *args, **kwargs):
        r = settings.REDIS_OBJ_SYNC
        if self.pk:
            old_status = Order.objects.get(pk=self.pk).status
            if old_status != self.status:
                payload = {
                    "tg_id": self.client_id,
                    "order_id": self.pk,
                    "new_status": self.status,
                }
                r.lpush("order_status_changed", json.dumps(payload))

        return super().save(*args, **kwargs)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    price_at_purchase = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)


class FAQ(models.Model):
    question = models.CharField(max_length=255)
    answer = models.TextField()
    active = models.BooleanField(default=True)


class GlobalSettings(models.Model):
    admin_tg_id = models.BigIntegerField(
        verbose_name="ID чата администратора", default=0
    )

    def __str__(self):
        return "Глобальные настройки системы"


class Newsletter(models.Model):
    class Status(models.TextChoices):
        ready = "ready", "Готова к отправке"
        sent = "sent", "Отправлена"
        draft = "draft", "Черновик"

    subject = models.CharField(
        "Тема (для админки)", max_length=255, help_text="Не отображается у пользователя"
    )
    text = models.TextField()
    image = models.ImageField(upload_to="newsletters/", null=True, blank=True)
    send_at = models.DateTimeField("Дата и время рассылки")

    status = models.CharField(
        choices=Status.choices, default=Status.ready, max_length=20
    )
    celery_task_id = models.CharField(
        max_length=255, null=True, blank=True, editable=False
    )

    class Meta:
        verbose_name = "Рассылка"
        verbose_name_plural = "Рассылки"

    def __str__(self):
        return f"{self.subject} ({self.send_at})"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if (
            self.pk
            and self.status == self.Status.ready
            or not self.pk
            and self.status == self.Status.ready
        ):
            payload = {
                "text": self.text,
                "image": self.image.url if self.image else None,
                "sent_at": self.send_at,
            }
            res = execute_newsletter_mailing.apply_async(
                args=[payload], eta=self.send_at
            )
            self.status = self.Status.sent
