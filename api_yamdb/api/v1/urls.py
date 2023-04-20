from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.v1.views import (
    CategoryViewSet,
    CommentViewSet,
    GenreViewSet,
    ReviewViewSet,
    TitleViewSet,
    UserViewSet,
    api_me,
    send_confirmation_code,
    get_jwt_token,
    UserDetailPach
)

router = DefaultRouter()

router.register(r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet, basename='review')
router.register(r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments', CommentViewSet, basename='comment')
router.register(r"titles", TitleViewSet)
router.register(r"categories", CategoryViewSet)
router.register(r"genres", GenreViewSet)
router.register(r"users", UserViewSet)

urlpatterns = [
    path("users/me/", api_me),
    path("", include(router.urls)),
    path('v1/auth/signup/', send_confirmation_code),
    path('v1/auth/token/', get_jwt_token),
    path('v1/users/me/', UserDetailPach.as_view()),
    path('v1/', include(router.urls)),
]
