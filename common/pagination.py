from rest_framework.pagination import PageNumberPagination

class GenericPagination(PageNumberPagination):
    page_size_query_param = 'size'