from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class LaravelStylePagination(PageNumberPagination):
    """
    Paginação customizada que imita o formato do Laravel ResourceCollection.
    Formato de saída:
    {
        "data": [...],
        "links": { "first": "...", "last": "...", "prev": null, "next": "..." },
        "meta": { "current_page": 1, "last_page": 50, "per_page": 20, "total": 1000 }
    }
    """
    page_size = 20
    page_query_param = 'page'

    def get_paginated_response(self, data):
        return Response({
            'data': data,
            'links': {
                'first': self.request.build_absolute_uri(
                    self.request.path + '?page=1'
                ),
                'last': self.request.build_absolute_uri(
                    self.request.path + f'?page={self.page.paginator.num_pages}'
                ),
                'prev': self.get_previous_link(),
                'next': self.get_next_link(),
            },
            'meta': {
                'current_page': self.page.number,
                'last_page': self.page.paginator.num_pages,
                'per_page': self.page_size,
                'from': self.page.start_index(),
                'to': self.page.end_index(),
                'total': self.page.paginator.count,
            }
        })

    def get_paginated_response_schema(self, schema):
        return {
            'type': 'object',
            'properties': {
                'data': schema,
                'links': {'type': 'object'},
                'meta': {'type': 'object'},
            }
        }
