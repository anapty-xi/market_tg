from django.urls import path
from views import (
    CartItemViews,
    CartViews,
    CategoryViews,
    OrderViews,
    ProductViews,
    ProfileViews,
    SubscriptionViews,
)

app_name = "market"

urlpatterns = [
    path("profile/", ProfileViews.as_view()),
    path("profile/<int:tg_id>/<str:username>/", ProfileViews.as_view()),
    path("subscription/", SubscriptionViews.as_view()),
    path("order/", OrderViews.as_view()),
    path("order/<int:order_id>/", OrderViews.as_view()),
    path("product/", ProductViews.as_view()),
    path("category/", CategoryViews.as_view()),
    path("cart_item/<int:tg_id>/", CartItemViews.as_view()),
    path("cart/<int:tg_id>/", CartViews.as_view()),
]
