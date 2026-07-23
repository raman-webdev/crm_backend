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


class MembershipSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    email = serializers.EmailField(
        source="user.email",
        read_only=True,
    )

    class Meta:
        model = Membership
        fields = (
            "id",
            "full_name",
            "email",
            "role",
            "joined_at",
        )
        read_only_fields = (
            "id",
            "full_name",
            "email",
            "joined_at",
        )

    def get_full_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}".strip()
    
