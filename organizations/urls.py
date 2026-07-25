from django.urls import path

from .views import (
    OrganizationListCreateView,
    OrganizationDetailView,
    InvitationView,
    InvitationDetailView,
    AcceptInvitationAPIView,
    MembershipListAPIView,
    MembershipDetailView,
)

urlpatterns = [
    # Organization
    path(
        "",
        OrganizationListCreateView.as_view(),
        name="organization-list-create",
    ),
    path(
        "<int:pk>/",
        OrganizationDetailView.as_view(),
        name="organization-detail",
    ),

    # Invitations
    path(
        "invitations/",
        InvitationView.as_view(),
        name="invite-member",
    ),
    path(
        "invitations/<uuid:token>/",
        InvitationDetailView.as_view(),
        name="invitation-detail",
    ),
    path(
        "invitations/<uuid:token>/accept/",
        AcceptInvitationAPIView.as_view(),
        name="invitation-accept",
    ),

    # Memberships
    path(
        "members/",
        MembershipListAPIView.as_view(),
        name="member-list",
    ),
    path(
        "members/<int:pk>/",
        MembershipDetailView.as_view(),
        name="member-detail",
    ),
]