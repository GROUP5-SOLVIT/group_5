from django.urls import path

from .views import ExpenseReportView, InventoryReportView, PurchaseReportView, SalesReportView

app_name = "reports"

urlpatterns = [
    path("sales/", SalesReportView.as_view(), name="sales"),
    path("inventory/", InventoryReportView.as_view(), name="inventory"),
    path("expenses/", ExpenseReportView.as_view(), name="expenses"),
    path("purchases/", PurchaseReportView.as_view(), name="purchases"),
]
