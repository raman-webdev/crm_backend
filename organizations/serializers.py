from rest_framework import serializers
from .models import Organization, Membership, Invitation

class OrganizationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Organization
        fields = [
            "id",
            "name",
            "address",
            "email",
            "phone",
            "is_active",
            "created_at",
        ]

        read_only = [
            "id",
            "is_active",
            "created_at",
        ]


class InviteMemberSerializer(serializers.Serializer):

    email = serializers.EmailField()

    role = serializers.ChoiceField(
        choices=Membership.ROLE_CHOICES,
    )


class InvitationDetailSerializer(serializers.ModelSerializer):
    organization = serializers.CharField(
        source="organization.name",
        read_only=True,
    )

    class Meta:
        model = Invitation
        fields = (
            "email",
            "role",
            "organization",
            "status",
            "expires_at",
        )