from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from organizations.helpers import (
    get_current_organization,
    require_roles,
)
from organizations.models import Membership

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

        serializer = ActivityLogSerializer(
            logs,
            many=True,
        )

        return Response(serializer.data)