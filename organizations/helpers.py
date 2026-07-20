from django.shortcuts import get_object_or_404

from rest_framework.exceptions import (
    PermissionDenied,
    ValidationError,
)

from .models import (
    Membership,
    Organization,
)


def get_current_organization(request):

    if not request.user.is_authenticated:
        raise PermissionDenied(
            "Authentication required."
        )
    

    organization_id = request.headers.get(
        "X-Organization-ID"
    )

    if not organization_id:
        raise ValidationError(
            {
                "organization": [
                    "X-Organization-ID header is required."
                ]
            }
        )
    
    membership = (
        Membership.objects.select_related("organization")
        .filter(
            organization_id=organization_id,
            user=request.user,
            is_active=True,
            organization__is_active=True,
        )
        .first()
    )

    if membership is None:
        raise PermissionDenied(
            "You do not have access to this organization."
        )
    

    return membership.organization, membership