from django.urls import path

from .views import (
    CartItemViews,
    CartViews,
    MainCategoryViews,
    OrderViews,
    ProductViews,
    ProfileViews,
    SubCategoryViews,
    SubscriptionViews,
)

app_name = "market"

urlpatterns = [
    path("profile/", ProfileViews.as_view()),
    path("profile/<int:tg_id>/<str:username>/", ProfileViews.as_view()),
    path("subscription/", SubscriptionViews.as_view()),
    path("order/", OrderViews.as_view()),
    path("order/<int:order_id>/", OrderViews.as_view()),
    path("products/<int:cat_id>/", ProductViews.as_view()),
    path("main_categories/", MainCategoryViews.as_view()),
    path("sub_categories/<int:main_cat_id>/", SubCategoryViews.as_view()),
    path("cart_item/<int:tg_id>/", CartItemViews.as_view()),
    path("cart/<int:tg_id>/", CartViews.as_view()),
]
