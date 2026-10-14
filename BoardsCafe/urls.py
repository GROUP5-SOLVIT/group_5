"""
URL configuration for BoardsCafe project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
"""
from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

urlpatterns = [
    path('', RedirectView.as_view(url='/api/v1/docs/', permanent=False), name='root'),
    path('admin/', admin.site.urls),
    path('api/v1/auth/', include('BoardsCafe.apps.users.urls')),
    path('api/v1/auth/otp/', include('BoardsCafe.apps.otp.urls')),
    path('api/v1/business/', include('BoardsCafe.apps.business.urls')),
    path('api/v1/roles/', include('BoardsCafe.apps.roles.urls')),
    path('api/v1/dashboard/', include('BoardsCafe.apps.dashboard.urls')),
    path('api/v1/menu/', include('BoardsCafe.apps.menu.urls')),
    path('api/v1/recipes/', include('BoardsCafe.apps.recipes.urls')),
    path('api/v1/inventory/', include('BoardsCafe.apps.inventory.urls')),
    path("api/v1/sales/", include("BoardsCafe.apps.sales.urls")),
    path('api/v1/purchasing/', include('BoardsCafe.apps.purchasing.urls')),
    path('api/v1/finance/', include('BoardsCafe.apps.finance.urls')),
    path('api/v1/reports/', include('BoardsCafe.apps.reports.urls')),
    path('api/v1/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/v1/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/v1/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    path('api/v1/health/', include('BoardsCafe.core.health_urls')),
]
