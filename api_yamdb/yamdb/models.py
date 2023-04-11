from django.db import models
from django.contrib.auth.models import AbstractUser

ROLES = [
    ("user", "Пользователь"),
    ("moderator", "Модератор"),
    ("admin", "Администратор"),
]


class Users(AbstractUser):
    bio = models.TextField("Биография", blank=True)
    role = models.CharField(choices=ROLES, max_length=9, default="user")
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=True, primary_key=True)


class Categories(models.Model):
    name = models.CharField(max_length=256, blank=False, null=False)
    slug = models.SlugField(
        max_length=50, blank=False, null=False, unique=True
    )


class Genres(models.Model):
    name = models.CharField(max_length=256, blank=False, null=False)
    slug = models.SlugField(
        max_length=50, blank=False, null=False, unique=True
    )


class Titles(models.Model):
    name = models.CharField(
        "Название", max_length=256, blank=False, null=False
    )
    year = models.IntegerField(
        "Год выпуска", blank=False, null=False
    )
    description = models.TextField("Описание")
    genre = models.ForeignKey(
        Genres,
        blank=False,
        null=False,
        on_delete=models.DO_NOTHING,
        related_name="titles",
    )
    category = models.ForeignKey(
        Categories,
        blank=False,
        null=False,
        on_delete=models.DO_NOTHING,
        related_name="titles",
    )
