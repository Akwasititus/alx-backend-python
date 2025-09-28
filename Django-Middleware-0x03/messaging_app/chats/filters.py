import django_filters
from .models import Message

class MessageFilter(django_filters.FilterSet):
    user = django_filters.NumberFilter(field_name="user__id", lookup_expr="exact")
    created_after = django_filters.DateTimeFilter(field_name="created_at", lookup_expr="gte")
    created_before = django_filters.DateTimeFilter(field_name="created_at", lookup_expr="lte")

    class Meta:
        model = Message
        fields = ["user", "created_after", "created_before"]
