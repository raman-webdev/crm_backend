from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from organizations.helpers import (
    get_current_organization,
    require_roles,
)
from organizations.models import Membership
from config.pagination import paginate_queryset

from .models import ActivityLog
from .serializers import ActivityLogSerializer


class ActivityLogListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):

        organization, membership = get_current_organization(request)

        require_roles(
            membership,
            Membership.OWNER,
            Membership.MANAGER,
        )

        logs = ActivityLog.objects.filter(
            organization=organization,
        ).select_related(
            "user",
        )

        result = paginate_queryset(
            logs,
            request,
        )

        serializer = ActivityLogSerializer(
            result["items"],
            many=True,
        )

        return Response(
    {
        "count": result["count"],
        "page": result["page"],
        "page_size": result["page_size"],
        "total_pages": result["total_pages"],
        "has_next": result["has_next"],
        "has_previous": result["has_previous"],
        "results": serializer.data,
    }
)