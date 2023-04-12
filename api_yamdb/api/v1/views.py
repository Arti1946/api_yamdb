from rest_framework import filters, mixins, viewsets
from rest_framework.permissions import IsAuthenticated

from django_filters.rest_framework import DjangoFilterBackend

from yamdb.models import Categories, Genres, Titles, Users
from api.v1.serializers import (
    CategorySerializer,
    GenreSerializer,
    TitleSerializer,
    UserSerializer,
)


class CategoryViewSet(viewsets.ModelViewSet):
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name",)
    queryset = Categories.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(viewsets.ModelViewSet):
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name",)
    queryset = Genres.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(viewsets.ModelViewSet):
    filter_backends = (DjangoFilterBackend,)
    queryset = Titles.objects.select_related("category")
    filterset_fields = ("category", "genre", "name", "year")
    serializer_class = TitleSerializer


class UserViewSet(viewsets.ModelViewSet):
    filter_backends = (filters.SearchFilter,)
    search_fields = ("username",)
    serializer_class = UserSerializer
    queryset = Users.objects.all()


class RetrieveUpdateViewSet(
    mixins.RetrieveModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet
):
    pass


class UserMeViewSet(RetrieveUpdateViewSet):
    serializer_class = UserSerializer
    permission_classes = IsAuthenticated

    def get_queryset(self):
        user = self.request.user
        new_queryset = Users.objects.filter(username=user)
        return new_queryset
