from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db import transaction


from .models import Customer
from .serializers import CustomerSerializer

from ..organizations.helpers import get_current_organization, require_roles
from ..organizations.models import Membership

# Create your views here.


class CustomerListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):

        organization, membership = get_current_organization(request)

        require_roles(
            Membership,
            Membership.OWNER,
            Membership.MANAGER,
            Membership.STAFF,
        )

        customers = Customer.objects.filter(
            organization=organization,
            is_active=True
        ).order_by("-created_at")

        serializer = CustomerSerializer(
            customers,
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

        serializer = CustomerSerializer(
            data=request.data
        )

        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]

        if Customer.objects.filter(
            organization=organization,
            email=email,
            is_active=True,
        ).exists():
            return Response(
                {
                    "detail": "Customer with this email already exists."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        customer = serializer.save(
            organization=organization,
            created_by=request.user,
        )

        return Response(
            {
                "detail": "Customer created successfully.",
                "data": CustomerSerializer(customer).data,
            },
            status=status.HTTP_201_CREATED,
        )





