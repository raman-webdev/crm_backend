def apply_ordering(
    queryset,
    request,
    default="-created_at",
    allowed_fields=None,
):
    """
    Apply ordering from query parameters.

    Example:
        ?ordering=name
        ?ordering=-created_at
    """

    ordering = request.query_params.get(
        "ordering",
        default,
    )

    if allowed_fields is None:
        allowed_fields = []

    field = ordering.lstrip("-")

    if field not in allowed_fields:
        ordering = default

    return queryset.order_by(ordering)