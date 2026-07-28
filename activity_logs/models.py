from django.db import models
from django.conf import settings

from organizations.models import Organization

# Create your models here.

class ActivityLog(models.Model):

    CUSTOMER_CREATED = "CUSTOMER_CREATED"
    CUSTOMER_UPDATED = "CUSTOMER_UPDATED"
    CUSTOMER_DELETED = "CUSTOMER_DELETED"

    TASK_CREATED = "TASK_CREATED"
    TASK_UPDATED = "TASK_UPDATED"
    TASK_COMPLETED = "TASK_COMPLETED"
    TASK_DELETED = "TASK_DELETED"

    ORGANIZATION_CREATED = "ORGANIZATION_CREATED"
    MEMBER_INVITED = "MEMBER_INVITED"

    ACTION_CHOICES = (
        (CUSTOMER_CREATED, "Customer Created"),
        (CUSTOMER_UPDATED, "Customer Updated"),
        (CUSTOMER_DELETED, "Customer Deleted"),
        (TASK_CREATED, "Task Created"),
        (TASK_UPDATED, "Task Updated"),
        (TASK_COMPLETED, "Task Completed"),
        (TASK_DELETED, "Task Deleted"),
        (ORGANIZATION_CREATED, "Organization Created"),
        (MEMBER_INVITED, "Member Invited"),
    )

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="activity_logs"
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="activity_logs"
    )

    action = models.CharField(
        max_length=100,
        choices=ACTION_CHOICES,
    )

    object_type = models.CharField(max_length=100)

    object_id = models.PositiveIntegerField()

    description = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user} - {self.action}"
