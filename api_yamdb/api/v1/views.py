from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, status, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404

from api.permissions import (
    IsAdmin,
    IsAdminOrReadOnly,
    IsAuthorOrAdminOrModeratorOrReadOnly,
)
from api.v1.filters import TitleFilter
from api.v1.serializers import (
    CategorySerializer,
    CheckCodeSerializer,
    CommentSerializer,
    GenreSerializer,
    ReviewSerializer,
    SendCodeSerializer,
    TitleSerializer,
    TitleSerializerPost,
    UserSerializer,
)
from reviews.models import Categories, Comments, Genres, Review, Title, Users


@api_view(["POST"])
def send_confirmation_code(request):
    serializer = SendCodeSerializer(data=request.data)
    if serializer.is_valid():
        username = serializer.validated_data.get("username")
        email = serializer.validated_data.get("email")
        token = PasswordResetTokenGenerator()
        if not Users.objects.filter(username=username, email=email).exists():
            if (
                Users.objects.filter(username=username).exists()
                or Users.objects.filter(email=email).exists()
            ):
                return Response(
                    {"result": "Этот email или username уже используются."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            Users.objects.create_user(username=username, email=email)
        user = Users.objects.get(username=username)
        code = token.make_token(user=user)
        send_mail(
            "Подтверждение аккаунта на Yamdb",
            f"Код подтверждения: {code}",
            None,
            [email],
            fail_silently=True,
        )
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def get_jwt_token(request):
    """
    Достает введеный код и сверяет с присвоенным юзеру.
    Возвращает токен для авторизации.
    """
    serializer = CheckCodeSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data.get("username")
    confirmation_code = serializer.validated_data.get("confirmation_code")
    user = get_object_or_404(Users, username=username)
    token = PasswordResetTokenGenerator()
    if token.check_token(user=user, token=confirmation_code):
        token = AccessToken.for_user(user)
        return Response({"token": f"{token}"}, status=status.HTTP_200_OK)
    return Response(
        {"confirmation_code": "Неверный код подтверждения"},
        status=status.HTTP_400_BAD_REQUEST,
    )


class ListCreateDeleteViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    pass


class CategoryViewSet(ListCreateDeleteViewSet):
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name",)
    queryset = Categories.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]
    lookup_field = "slug"


class GenreViewSet(ListCreateDeleteViewSet):
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name",)
    queryset = Genres.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAdminOrReadOnly]
    lookup_field = "slug"


class TitleViewSet(viewsets.ModelViewSet):
    filter_backends = (DjangoFilterBackend,)
    queryset = (
        Title.objects.annotate(rating=Avg("reviews__score"))
        .select_related(
            "category",
        )
        .prefetch_related("genre")
    )
    filterset_fields = ("genre", "year", "name", "category")
    filterset_class = TitleFilter
    permission_classes = [IsAdminOrReadOnly]

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return TitleSerializer
        return TitleSerializerPost


class UserViewSet(viewsets.ModelViewSet):
    filter_backends = (filters.SearchFilter,)
    search_fields = ("username",)
    serializer_class = UserSerializer
    queryset = Users.objects.all()
    permission_classes = [IsAdmin]
    lookup_field = "username"
    http_method_names = ["get", "post", "head", "patch", "delete"]


class UserDetailPach(APIView):
    def get(self, request):
        if request.user.is_anonymous:
            return Response(
                "Вы не авторизованы", status=status.HTTP_401_UNAUTHORIZED
            )
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    def patch(self, request):
        if request.user.is_anonymous:
            return Response(
                "Вы не авторизованы", status=status.HTTP_401_UNAUTHORIZED
            )
        serializer = UserSerializer(
            request.user, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(role=request.user.role)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthorOrAdminOrModeratorOrReadOnly]

    def get_queryset(self):
        title_id = self.kwargs.get("title_id")
        return Review.objects.select_related("author").filter(title=title_id)

    def perform_create(self, serializer):
        title_id = self.kwargs.get("title_id")
        title = get_object_or_404(Title, pk=title_id)
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthorOrAdminOrModeratorOrReadOnly]

    def get_queryset(self):
        review_id = self.kwargs.get("review_id")
        return Comments.objects.select_related("author").filter(
            review=review_id
        )

    def perform_create(self, serializer):
        review_id = self.kwargs.get("review_id")
        user = self.request.user
        review = get_object_or_404(Review, pk=review_id)
        serializer.save(author=user, review=review)
