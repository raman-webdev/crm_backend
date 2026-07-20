from django.db import models
from django.conf import settings

# Create your models here.

class Organization(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField(blank=True)
    email = models.EmailField()
    phone = models.CharField(max_length=30)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    

class Membership(models.Model):

    OWNER = "OWNER"
    MANAGER = "MANAGER"
    STAFF = "STAFF"

    ROLE_CHOICES = (
        (OWNER, "Owner"),
        (MANAGER, "Manager"),
        (STAFF, "Staff"),
    )

    user = models.ForeignKey(
        'accounts.User',
        on_delete=models.CASCADE,
        related_name="memberships"
    )
    organization = models.ForeignKey(
        "organizations.Organization",
        on_delete=models.CASCADE,
        related_name="memberships"
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
    )

    is_active = models.BooleanField(default=True)

    joined_at = models.DateTimeField(auto_now_add=True)