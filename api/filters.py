from django_filters import rest_framework as filters
from .models import Link


class LinkFilter(filters.FilterSet):
    owner = filters.CharFilter(field_name="owner__email")
    visit_count_max = filters.NumberFilter(
        field_name="visit_count",
        lookup_expr="gte",
        label="Minimum Visit Count")
    visit_count_min = filters.NumberFilter(
        field_name="visit_count",
        lookup_expr="lte",
        label="Max Visit Count")
    date_created_min = filters.DateFilter(
        field_name="date_created",
        lookup_expr="gte",
        label="Date Created Greater Than")
    date_created_max = filters.DateFilter(
        field_name="date_created",
        lookup_expr="lte",
        label="Date Created Less Than")

    class Meta:
        model = Link
        exclude = ["long_link"]
