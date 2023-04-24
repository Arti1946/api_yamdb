from rest_framework.routers import DefaultRouter

from django.urls import include, path

from api.v1.views import (
    CategoryViewSet, CommentViewSet, GenreViewSet, ReviewViewSet, TitleViewSet,
    UserDetailPach, UserViewSet, get_jwt_token, send_confirmation_code,
)

router = DefaultRouter()

router.register(
    r"titles/(?P<title_id>\d+)/reviews", ReviewViewSet, basename="review"
)
router.register(
    r"titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments",
    CommentViewSet,
    basename="comment",
)
router.register(r"titles", TitleViewSet)
router.register(r"categories", CategoryViewSet)
router.register(r"genres", GenreViewSet)
router.register(r"users", UserViewSet)

urlpatterns = [
    path("users/me/", UserDetailPach.as_view()),
    path("", include(router.urls)),
    path("auth/signup/", send_confirmation_code),
    path("auth/token/", get_jwt_token),
]
