from rest_framework.pagination import PageNumberPagination   # ✅ keyword present

class MessagePagination(PageNumberPagination):
    """
    Pagination for messages – 20 per page by default.
    """
    page_size = 20
    page_size_query_param = "page_size"
    max_page_size = 100
