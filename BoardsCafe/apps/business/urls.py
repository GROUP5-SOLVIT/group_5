from django.urls import path
from .views import (
    BusinessProfileListCreateView, BusinessProfileDetailView,
    FloorListCreateView, FloorDetailView,
    TableListCreateView, TableDetailView,
    PaymentMethodListCreateView, PaymentMethodDetailView,
    BusinessConfigurationDetailView, business_config_defaults
)

app_name = 'business'

urlpatterns = [
    # Business Profile
    path('', BusinessProfileListCreateView.as_view(), name='business-list-create'),
    path('<int:pk>/', BusinessProfileDetailView.as_view(), name='business-detail'),

    # Business Configuration
    path('<int:business_pk>/configuration/', BusinessConfigurationDetailView.as_view(), name='business-configuration'),
    path('configuration/defaults/', business_config_defaults, name='business-config-defaults'),

    # Floors
    path('<int:business_pk>/floors/', FloorListCreateView.as_view(), name='floor-list-create'),
    path('<int:business_pk>/floors/<int:pk>/', FloorDetailView.as_view(), name='floor-detail'),

    # Tables
    path('<int:business_pk>/floors/<int:floor_pk>/tables/', TableListCreateView.as_view(), name='table-list-create'),
    path('<int:business_pk>/floors/<int:floor_pk>/tables/<int:pk>/', TableDetailView.as_view(), name='table-detail'),

    # Payment Methods
    path('payment-methods/', PaymentMethodListCreateView.as_view(), name='payment-method-list-create'),
    path('payment-methods/<int:pk>/', PaymentMethodDetailView.as_view(), name='payment-method-detail'),
]