from django.db import transaction
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import PermissionDenied
from django.utils import timezone
from datetime import timedelta

from .models import Organization, Membership, Invitation
from .serializers import OrganizationSerializer, InviteMemberSerializer, InvitationDetailSerializer
from .helpers import get_current_organization, require_roles
from ..accounts.models import User


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
        organization, membership = get_current_organization(request)

        if organization.id != pk:
            raise PermissionDenied(
                "Invalid organization."
            )

        require_roles(
            membership,
            Membership.OWNER,
        )

        serializer = OrganizationSerializer(
            organization,
            data=request.data,
            partial=True,
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)
    


class InvitationView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):

        organization, membership = get_current_organization(request)

        require_roles(
            membership,
            membership.OWNER,
            membership.MANAGER,
        )

        serializer = InviteMemberSerializer(
            data=request.data
        )

        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        role = serializer.validated_data["role"]

        existing = Invitation.objects.filter(
            organization=organization,
            email=email,
            status=Invitation.PENDING,
        ).exists()

        if existing:
            return Response(
                {
                    "detail": "A pending invitation already exists."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        
        user = User.objects.filter(
            email=email
        ).first()

        if user:
            already_member = Membership.objects.filter(
                organization=organization,
                user=user,
                is_active=True,
            ).exists()

            if already_member:
                return Response(
                    {
                        "detail": "User is already a member."
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
            
        Invitation.objects.filter(
            organization=organization,
            email=email,
            status=Invitation.PENDING,
        ).exists()
            
        invitation = Invitation.objects.create(
            organization=organization,
            email=email,
            role=role,
            invited_by=request.user,
            expires_at=timezone.now()+timedelta(days=7)
        )

        return Response(
            {
                "message": "Invitation created successfully!",
                "token": str(invitation.token),
            },
            status=status.HTTP_201_CREATED,
        )


class InvitationDetailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, token):
        
        invitation = get_object_or_404(
            Invitation,
            tok=token,
        )

        if invitation.status != Invitation.PENDING:
            return Response(
                {
                    "detail": "Invitation is no longer valid."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        
        if invitation.is_expired:
            invitation.status = Invitation.EXPIRED
            invitation.save(update_fields=["status"])

            return Response(
                {
                    "detail": "Invitation has expired."
                },
                status=400,
            )
        
        serializer = InvitationDetailSerializer(invitation)

        return Response(
            {
                "invitation": serializer.data,
                "user_exists": User.objects.filter(
                    email=invitation.email
                ).exists(),
            }
        )
        