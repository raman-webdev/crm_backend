from .models import ActivityLog


def log_activity(
    organization,
    user,
    action,
    obj,
    description="",
):
    ActivityLog.objects.create(
        organization=organization,
        user=user,
        action=action,
        object_type=obj.__class__.__name__,
        object_id=obj.pk,
        description=description,
    )