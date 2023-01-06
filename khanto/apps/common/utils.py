import random
import string

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class OptionalNumberPagePagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = "page_size"

    def paginate_queryset(self, queryset, request, view=None):
        if "no_page" in request.query_params:
            return None
        return super().paginate_queryset(queryset, request, view)

    def get_paginated_response(self, data):
        return Response(
            {
                "links": {
                    "next": self.get_next_link(),
                    "previous": self.get_previous_link(),
                },
                "count": self.page.paginator.count,
                "total_pages": self.page.paginator.num_pages,
                "results": data,
            }
        )


def get_random_string(length):
    # Generate a random string with numbers and capitalize letters of fixed length
    characters = string.ascii_uppercase + string.digits
    return "".join(random.choice(characters) for _ in range(length))
