from rest_framework import serializers
from .models import Task


class TaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = (
            "id",
            "customer",
            "assigned_to",
            "title",
            "description",
            "priority",
            "due_date",
            "status",
            "created_at",
            "updated_at",
        )

        read_only_fields = (
            "id",
            "created_at",
            "updated_at",
        )

        def validate_due_date(self, value):
            from django.utils import timezone

            if value < timezone.localdate():
                raise serializers.ValidationError(
                    "Due date cannot be in the past."
                )

            return value