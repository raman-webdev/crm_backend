from django.urls import path
from .views import OrganizationListCreateView, OrganizationDetailView, InvitationView, InvitationDetailView, AcceptInvitationAPIView


urlpatterns = [
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
]