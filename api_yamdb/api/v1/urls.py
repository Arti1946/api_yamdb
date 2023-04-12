from rest_framework import routers

from django.urls import include, path

from api.v1.views import (
    TitleViewSet,
    CategoryViewSet,
    GenreViewSet,
    UserViewSet,
    UserMeViewSet,
)

router = routers.DefaultRouter()

router.register(r"titles", TitleViewSet)
router.register(r"categories", CategoryViewSet)
router.register(r"genres", GenreViewSet)
router.register(r"users", UserViewSet)
router.register(r"users/me", UserMeViewSet, basename="me")

urlpatterns = [
    path("", include(router.urls)),
]
