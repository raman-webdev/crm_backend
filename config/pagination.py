from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator


def paginate_queryset(queryset, request, page_size=10):
    """
    Reusable pagination helper.
    """

    page = request.query_params.get("page", 1)

    page_size = request.query_params.get(
        "page_size",
        page_size,
    )

    try:
        page_size = int(page_size)
    except ValueError:
        page_size = 10

    paginator = Paginator(
        queryset,
        page_size,
    )

    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    return {
        "items": page_obj.object_list,
        "count": paginator.count,
        "page": page_obj.number,
        "page_size": page_size,
        "total_pages": paginator.num_pages,
        "has_next": page_obj.has_next(),
        "has_previous": page_obj.has_previous(),
    }