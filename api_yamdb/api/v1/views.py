import uuid
from rest_framework import filters, viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from api_yamdb.settings import YAMBD_EMAIL
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken

from yamdb.models import Users, Titles, Categories, Genres, Reviews, Comments
from api.v1.serializers import (
    TitleSerializer, CategorySerializer, GenreSerializer,
    ReviewSerializer, CommentSerializer, UserSerializer, SendCodeSerializer, CheckCodeSerializer
)
from api.permissions import IsAdmin, IsAdminOrReadOnly, IsAuthorOrAdminOrModeratorOrReadOnly


@api_view(['POST'])
def send_confirmation_code(request):
    serializer = SendCodeSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data.get('username')
    email = serializer.validated_data.get('email')
    if not Users.objects.filter(username=username, email=email).exists():
        if (
                Users.objects.filter(username=username).exists()
                or Users.objects.filter(email=email).exists()
        ):
            return Response(
                {"result": "Этот email или username уже используются."},
                status=status.HTTP_400_BAD_REQUEST
            )
        Users.objects.create_user(username=username, email=email)
    user = Users.objects.get(username=username)
    user.confirmation_code = uuid.uuid4()
    user.save()
    send_mail(
        'Подтверждение аккаунта на Yamdb',
        f'Код подтверждения: {user.confirmation_code}',
        YAMBD_EMAIL,
        [email],
        fail_silently=True,
    )
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def get_jwt_token(request):
    '''
    Достает введеный код и сверяет с присвоенным юзеру.
    Возвращает токен для авторизации.
    '''
    serializer = CheckCodeSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data.get('username')
    confirmation_code = serializer.validated_data.get('confirmation_code')
    user = get_object_or_404(Users, username=username)
    if confirmation_code == user.confirmation_code:
        token = AccessToken.for_user(user)
        return Response(
            {'token': f'{token}'},
            status=status.HTTP_200_OK
        )
    return Response(
        {'confirmation_code': 'Неверный код подтверждения'},
        status=status.HTTP_400_BAD_REQUEST
    )


class CategoryViewSet(viewsets.ModelViewSet):
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name",)
    queryset = Categories.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]


class GenreViewSet(viewsets.ModelViewSet):
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name",)
    queryset = Genres.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAdminOrReadOnly]


class TitleViewSet(viewsets.ModelViewSet):
    filter_backends = (DjangoFilterBackend,)
    queryset = Titles.objects.select_related("category")
    filterset_fields = ("category", "genre", "name", "year")
    serializer_class = TitleSerializer
    permission_classes = [IsAdminOrReadOnly]


class UserViewSet(viewsets.ModelViewSet):
    filter_backends = (filters.SearchFilter,)
    search_fields = ("username",)
    serializer_class = UserSerializer
    queryset = Users.objects.all()
    permission_classes = [IsAdmin]


class UserDetailPach(APIView):
    def get(self, request):
        if request.user.is_anonymous:
            return Response(
                'Вы не авторизованы', status=status.HTTP_401_UNAUTHORIZED
            )
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    def patch(self, request):
        if request.user.is_anonymous:
            return Response(
                'Вы не авторизованы', status=status.HTTP_401_UNAUTHORIZED
            )
        serializer = UserSerializer(
            request.user,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(role=request.user.role)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthorOrAdminOrModeratorOrReadOnly]

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        return Reviews.objects.filter(title_id=title_id)

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        serializer.save(author=self.request.user, title_id=title_id)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthorOrAdminOrModeratorOrReadOnly]

    def get_queryset(self):
        review_id = self.kwargs.get('review_id')
        return Comments.objects.filter(review_id=review_id)

    def perform_create(self, serializer):
        review_id = self.kwargs.get('review_id')
        serializer.save(author=self.request.user, review_id=review_id)
