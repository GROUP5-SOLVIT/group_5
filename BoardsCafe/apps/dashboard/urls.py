from django.urls import path

from .views import DashboardSummaryView

app_name = "dashboard"

urlpatterns = [
    path("", DashboardSummaryView.as_view(), name="summary"),
]
