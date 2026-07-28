from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from django.shortcuts import get_object_or_404


from .models import Customer
from .serializers import CustomerSerializer

from organizations.helpers import get_current_organization, require_roles
from organizations.models import Membership
from activity_logs.helpers import log_activity
from activity_logs.models import ActivityLog
from config.pagination import paginate_queryset

# Create your views here.


class CustomerListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):

        organization, membership = get_current_organization(request)

        require_roles(
            membership,
            Membership.OWNER,
            Membership.MANAGER,
            Membership.STAFF,
        )

        customers = Customer.objects.filter(
            organization=organization,
            is_active=True
        ).order_by("-created_at")

        result = paginate_queryset(
            customers,
            request,
        )

        serializer = CustomerSerializer(
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

        log_activity(
    organization=organization,
    user=request.user,
    action=ActivityLog.CUSTOMER_CREATED,
    obj=customer,
    description=f"Created customer '{customer.name}'.",
)

        return Response(
            {
                "detail": "Customer created successfully.",
                "data": CustomerSerializer(customer).data,
            },
            status=status.HTTP_201_CREATED,
        )



class CustomerDetailView(APIView):
    permission_classes = [IsAuthenticated]


    def get(self, request, pk):

        organization, membership = get_current_organization(request)

        require_roles(
            membership,
            Membership.OWNER,
            Membership.MANAGER,
            Membership.STAFF,
        )

        customer = get_object_or_404(
            Customer,
            organization=organization,
            pk=pk,
            is_active=True,
        )

        serializer = CustomerSerializer(
            customer,
        )

        return Response(
            serializer.data
        )


    def patch(self, request, pk):

        organization, membership = get_current_organization(request)

        require_roles(
            membership,
            Membership.OWNER,
            Membership.MANAGER,
        )

        customer = get_object_or_404(
            Customer,
            organization=organization,
            pk=pk,
            is_active=True,
        )

        serializer = CustomerSerializer(
            customer,
            data=request.data,
            partial=True,
        )

        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data.get["email"]

        if email:
            exists = Customer.objects.filter(
                organization=organization,
                email=email,
                is_active=True,
            ).exclude(pk=customer.pk).exists()

            if exists:
                return Response(
                    {
                        "detail": "Customer with this email already exists.",
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        serializer.save()

        return Response(serializer.data)


    def delete(self, request, pk):

        organization, membership = get_current_organization(request)

        require_roles(
            membership,
            Membership.OWNER,
            Membership.MANAGER,
        )

        customer = get_object_or_404(
            Customer,
            organization=organization,
            pk=pk,
            is_active=True,
        )

        customer.is_active = False
        customer.save(update_fields=["is_active"])

        return Response(
            {
                 "message": "Customer removed successfully.",
            },
            status=status.HTTP_200_OK
        )