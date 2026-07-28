def apply_filters(queryset, request, allowed_filters):
    """
    Apply exact-match filters from query parameters.

    Example:
        allowed_filters = [
            "status",
            "priority",
            "assigned_to",
        ]
    """

    for field in allowed_filters:

        value = request.query_params.get(field)

        if value not in (None, ""):
            queryset = queryset.filter(**{field: value})

    return queryset