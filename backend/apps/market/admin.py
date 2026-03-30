from apps.market.models import (
    FAQ,
    CartItem,
    Category,
    GlobalSettings,
    Newsletter,
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


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ["user", "product", "quantity"]


@admin.register(GlobalSettings)
class GlobalSettingsAdmin(admin.ModelAdmin):
    list_display = ["admin_tg_id"]


# 1. Создаем Inline класс для изображений
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    fields = ["image"]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", "price", "category", "get_image_count"]
    list_filter = ["category", "price"]
    search_fields = ["name", "description"]
    inlines = [ProductImageInline]

    def get_image_count(self, obj):
        return obj.images.count()

    get_image_count.short_description = "Кол-во фото"


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1
    fields = ["product", "quantity", "price_at_purchase"]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["id", "status", "client", "client_full_name", "created_at"]
    list_filter = ["status", "created_at"]
    search_fields = ["client_full_name", "client__username", "address"]
    inlines = [OrderItemInline]
    list_editable = ["status"]
    fieldsets = (
        ("Основная информация", {"fields": ("status", "client", "created_at")}),
        (
            "Данные доставки",
            {
                "fields": ("client_full_name", "address"),
            },
        ),
    )
    readonly_fields = ["created_at"]


@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = (
        "subject",
        "send_at",
        "status",
    )
