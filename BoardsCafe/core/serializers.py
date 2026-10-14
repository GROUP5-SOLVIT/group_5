from rest_framework import serializers


class ActionDetailSerializer(serializers.Serializer):
    detail = serializers.CharField()


class HealthCheckDataSerializer(serializers.Serializer):
    status = serializers.CharField(help_text='healthy when all checks pass; otherwise degraded')
    database = serializers.ChoiceField(choices=('healthy', 'unhealthy'))
    version = serializers.CharField()


class HealthCheckResponseSerializer(serializers.Serializer):
    success = serializers.BooleanField()
    message = serializers.CharField()
    data = HealthCheckDataSerializer()
