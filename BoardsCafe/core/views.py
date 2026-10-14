from rest_framework import status
from rest_framework import generics
from rest_framework.permissions import AllowAny
from django.db import connection
from django.conf import settings
from drf_spectacular.utils import extend_schema

from .responses import success_response
from .serializers import HealthCheckResponseSerializer


@extend_schema(responses={200: HealthCheckResponseSerializer, 503: HealthCheckResponseSerializer})
class HealthCheckView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    authentication_classes = []
    serializer_class = HealthCheckResponseSerializer

    def get(self, request):
        db_status = 'healthy'
        try:
            with connection.cursor() as cursor:
                cursor.execute('SELECT 1')
        except Exception:
            db_status = 'unhealthy'

        data = {
            'status': 'healthy' if db_status == 'healthy' else 'degraded',
            'database': db_status,
            'version': '1.0.0',
        }

        http_status = status.HTTP_200_OK if db_status == 'healthy' else status.HTTP_503_SERVICE_UNAVAILABLE
        return success_response(data, "Board's Cafe API is running.", http_status)
