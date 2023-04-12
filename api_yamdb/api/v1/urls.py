from rest_framework import routers

from django.urls import include, path

from api.v1.views import (
    TitleViewSet,
    CategoryViewSet,
    GenreViewSet,
    UserViewSet,
    api_me,
)

router = routers.DefaultRouter()

router.register(r"titles", TitleViewSet)
router.register(r"categories", CategoryViewSet)
router.register(r"genres", GenreViewSet)
router.register(r"users", UserViewSet)

urlpatterns = [
    path("users/me/", api_me),
    path("", include(router.urls)),
]
