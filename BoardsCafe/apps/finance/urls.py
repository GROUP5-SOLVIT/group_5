from rest_framework.routers import DefaultRouter

from .views import ExpenseCategoryViewSet, ExpenseViewSet, PaymentViewSet

app_name = "finance"

router = DefaultRouter()
router.register("expense-categories", ExpenseCategoryViewSet, basename="expense-category")
router.register("expenses", ExpenseViewSet, basename="expense")
router.register("payments", PaymentViewSet, basename="payment")

urlpatterns = router.urls
