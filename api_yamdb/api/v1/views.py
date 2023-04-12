from rest_framework import filters, viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response

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


@api_view(["GET", "PATCH"])
def api_me(request):
    me = request.user.username
    info = Users.objects.get(username=me)
    if request.method == "PATCH":
        serializer = UserSerializer(info, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    serializer = UserSerializer(info)
    return Response(serializer.data)
