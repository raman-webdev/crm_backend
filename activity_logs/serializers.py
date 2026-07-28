from rest_framework import serializers

from .models import ActivityLog


class ActivityLogSerializer(serializers.ModelSerializer):

    user = serializers.StringRelatedField()

    class Meta:
        model = ActivityLog
        fields = (
            "id",
            "user",
            "action",
            "object_type",
            "object_id",
            "description",
            "created_at",
        )