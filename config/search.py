from django.db.models import Q


def apply_search(queryset, search, fields):
    """
    Apply search across multiple model fields.

    Args:
        queryset: QuerySet
        search: search string
        fields: list of field names

    Example:
        apply_search(queryset, "raman", ["name", "email"])
    """

    if not search:
        return queryset

    query = Q()

    for field in fields:
        query |= Q(**{f"{field}__icontains": search})

    return queryset.filter(query)