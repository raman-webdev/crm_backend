from django.db import transaction
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404

from .models import Organization, Membership
from .serializers import OrganizationSerializer


class OrganizationListCreateView(APIView):
    permission_classes =  [IsAuthenticated]

    def get(self, request):
        organizations = Organization.objects.filter(
            memberships__user=request.user,
            memberships__is_active=True,
            is_active=True,
        ).distinct()

        serializer = OrganizationSerializer(
            organizations,
            many=True,
        )

        return Response(
            {
                "success": True,
                "data": serializer.data,
            }
        )
    
    @transaction.atomic
    def post(self, request):
        serializer = OrganizationSerializer(
            data=request.data
        )

        serializer.is_valid(raise_exception=True)

        organization = serializer.save()

        Membership.objects.create(
            organization=organization,
            user=request.user,
            role=Membership.OWNER,
        )

        return Response(
            {
                "success": True,
                "message": "Organization Created Successfully.",
                "data": OrganizationSerializer(organization).data,
            },
            status=status.HTTP_201_CREATED,
        )
    

class OrganizationDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        membership = get_object_or_404(
            Membership,
            organization_id=pk,
            user=request.user,
            is_active=True,
            organization__is_active=True,
        )

        serializer = OrganizationSerializer(
            membership.organization
        )

        return Response(
            {
                "success": True,
                "data": serializer.data,
            }
        )
    
    def patch(self, request, pk):
        membership = get_object_or_404(
            Membership,
            organization_id=pk,
            user=request.user,
            role=Membership.OWNER,
            is_active=True,
            organization__is_active=True,
        )

        serializer = OrganizationSerializer(
            membership.organization,
            data=request.data,
            partial=True,
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {
                "success": True,
                "message": "Organization updated successfully.",
                "data": serializer.data,
            }
        )