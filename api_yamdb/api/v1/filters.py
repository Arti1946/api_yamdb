from django_filters import rest_framework as filters

from reviews.models import Title


class CharFilterInFilter(filters.BaseInFilter, filters.CharFilter):
    pass


class TitleFilter(filters.FilterSet):
    genre = CharFilterInFilter(field_name="genre__slug", lookup_expr="in")
    year = filters.NumberFilter(field_name="year", lookup_expr="exact")
    category = CharFilterInFilter(
        field_name="category__slug", lookup_expr="in"
    )
    name = CharFilterInFilter(field_name="name", lookup_expr="in")

    class Meta:
        fields = ("genre", "year", "name", "category")
        model = Title
