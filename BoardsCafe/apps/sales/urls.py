from rest_framework.routers import DefaultRouter

from .views import OrderViewSet

router = DefaultRouter()
router.register("orders", OrderViewSet, basename="order")

app_name = "sales"

urlpatterns = router.urls
