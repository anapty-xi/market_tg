import json

from apps.market.infrastructure.cart_infrastructure import CartDBGW
from apps.market.infrastructure.order_infrastructure import OrderDBGW
from apps.market.infrastructure.product_infrastructure import ProductDBGW
from apps.market.infrastructure.profile_infrastructure import ProfileDBGW
from apps.market.infrastructure.subscription_infrastructure import SubscriptionDVGW
from apps.market.usecases.cart.cart_usecases import (
    AddToCart,
    ChangeAmount,
    DelCart,
    DelFromCart,
    GetCart,
)
from apps.market.usecases.order.order_usecases import (
    ChangeStatus,
    CreateOrder,
    GetAllActiveOrders,
)
from apps.market.usecases.product.product_usecases import GetCategories, GetProducts
from apps.market.usecases.profile.profile_usecases import AddProfile, HasPhoneNumber
from apps.market.usecases.subscription.subscription_usecases import GetSubscriptions
from django.http import JsonResponse
from django.views import View


class ProfileViews(View):
    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.inf = ProfileDBGW()

    async def post(self, request):
        body = json.loads(request.body)

        usecase = AddProfile(self.inf)

        await usecase.execute(body["tg_id"], body["username"], body["phone_number"])

        return JsonResponse({"result": "profile created"}, status=201)

    async def get(self, request, tg_id: int, username: str):
        usecase = HasPhoneNumber(self.inf)
        phone_num = await usecase.execute(tg_id, username)

        if phone_num:
            return JsonResponse({"meessage": "ok"}, status=200)
        return JsonResponse({"message": "user does not have profile"}, status=404)


class SubscriptionViews(View):
    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.inf = SubscriptionDVGW()

    async def get(self, request):
        usecase = GetSubscriptions(self.inf)
        subs = await usecase.execute()

        if subs:
            return JsonResponse([s.model_dump() for s in subs], safe=False)
        else:
            return JsonResponse({"result": "no subscriptions"}, status=404)


class OrderViews(View):
    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.inf = OrderDBGW()

    async def post(self, request):
        body = json.loads(request.body)

        usecase = CreateOrder(self.inf)

        await usecase.execute(body["tg_id"], body["address"], body["client_full_name"])

        return JsonResponse({"result": "order_created"}, status=201)

    async def patch(self, request, order_id: int):
        status = request.GET.get("status")

        usecase = ChangeStatus(self.inf)

        await usecase.execute(order_id, status)

        return JsonResponse({"message": "status changed"}, status=200)

    async def get(self, request):
        usecase = GetAllActiveOrders(self.inf)
        orders = await usecase.execute()

        if orders:
            return JsonResponse([ord.model_dump() for ord in orders], safe=False)
        return JsonResponse({"message": "no active orders"}, status=404)


class ProductViews(View):
    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.inf = ProductDBGW()

    async def get(self, request):
        usecase = GetProducts(self.inf)
        products = await usecase.execute()

        if products:
            return JsonResponse(
                [p.model_dump() for p in products], status=200, safe=False
            )
        return JsonResponse({"message": "no products"}, status=404)


class CategoryViews(View):
    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.inf = ProductDBGW()

    async def get(self, request):
        usecase = GetCategories(self.inf)
        categories = await usecase.execute()

        if categories:
            return JsonResponse(
                [c.model_dump() for c in categories], status=200, safe=False
            )
        return JsonResponse({"message": "no categories"}, status=404)


class CartItemViews(View):
    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.inf = CartDBGW()

    async def post(self, request, tg_id: int):
        prod_id = request.GET.get("prod_id")

        usecase = AddToCart(self.inf)
        await usecase.execute(tg_id, prod_id)

        return JsonResponse({"message": "product added"}, status=201)

    async def delete(self, request, tg_id: int):
        prod_id = request.GET.get("prod_id")

        usecase = DelFromCart(self.inf)
        await usecase.execute(tg_id, prod_id)

        return JsonResponse({"message": "product deleted"}, status=200)

    async def patch(self, request, tg_id: int):
        prod_id = request.GET.get("prod_id")
        increase = request.GET.get("increase") == "True"

        usecase = ChangeAmount(self.inf)
        await usecase.execute(tg_id, prod_id, increase)

        return JsonResponse({"message": "amount changed"}, status=200)


class CartViews(View):
    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.inf = CartDBGW()

    async def get(self, request, tg_id: int):
        usecase = GetCart(self.inf)
        cart_items = await usecase.execute(tg_id)

        if cart_items:
            return JsonResponse(
                [item.model_dump() for item in cart_items], status=200, safe=False
            )
        return JsonResponse({"message": "no cart items for user"}, status=404)

    async def delete(self, request, tg_id: int):
        usecase = DelCart(self.inf)
        await usecase.execute(tg_id)

        return JsonResponse({"message": "cart deleted"}, status=200)
