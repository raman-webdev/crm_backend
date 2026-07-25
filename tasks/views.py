from django.db import transaction
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from organizations.helpers import (
    get_current_organization,
    require_roles,
)
from organizations.models import Membership

from customers.models import Customer
from accounts.models import User

from .models import Task
from .serializers import TaskSerializer


class TaskListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):

        organization, membership = get_current_organization(request)

        require_roles(
            membership,
            Membership.OWNER,
            Membership.MANAGER,
            Membership.STAFF,
        )

        if membership.role == Membership.STAFF:
            tasks = Task.objects.filter(
                organization=organization,
                assigned_to=request.user,
                is_active=True,
            ).order_by("-created_at")
        else:
            tasks = Task.objects.filter(
                organization=organization,
                is_active=True,
            ).order_by("-created_at")

        serializer = TaskSerializer(
            tasks,
            many=True,
        )

        return Response(serializer.data)

    @transaction.atomic
    def post(self, request):

        organization, membership = get_current_organization(request)

        require_roles(
            membership,
            Membership.OWNER,
            Membership.MANAGER,
        )

        serializer = TaskSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        customer = serializer.validated_data["customer"]
        assigned_to = serializer.validated_data["assigned_to"]

        # Validate customer belongs to current organization
        if (
            customer.organization != organization
            or not customer.is_active
        ):
            return Response(
                {
                    "detail": "Customer does not belong to this organization."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Validate assigned user belongs to current organization
        member_exists = Membership.objects.filter(
            organization=organization,
            user=assigned_to,
            is_active=True,
        ).exists()

        if not member_exists:
            return Response(
                {
                    "detail": "Assigned user does not belong to this organization."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        task = serializer.save(
            organization=organization,
            created_by=request.user,
        )

        return Response(
            {
                "detail": "Task created successfully.",
                "data": TaskSerializer(task).data,
            },
            status=status.HTTP_201_CREATED,
        )