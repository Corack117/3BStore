from django.urls import include, path
from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter
from applications.orders.views import OrderViewSet
from applications.products.views import ProductViewSet
from applications.users.views import UserViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    round = SimpleRouter()

router.register("orders", OrderViewSet, basename='orders')
router.register("products", ProductViewSet, basename='products')
router.register("users", UserViewSet, basename='users')

urlpatterns = [
    path('', include(router.urls)),
    path('inventories/product/<str:sku>/', ProductViewSet.as_view({'patch': 'add_to_inventory'}), name='add-to-inventory'),
]