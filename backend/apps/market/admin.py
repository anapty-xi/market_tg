from apps.market.models import (
    FAQ,
    CartItem,
    Category,
    Order,
    OrderItem,
    Product,
    ProductImage,
    Profile,
    Subscription,
)
from django.contrib import admin


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ["question", "answer"]


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ["tg_id", "username", "phone_number"]


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ["name", "channel_id", "link"]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "parent"]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", "description", "price", "category"]


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ["product", "image"]


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ["user", "product", "quantity"]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["status", "client", "address", "client_full_name", "created_at"]


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ["order", "product", "price_at_purchase", "quantity"]
