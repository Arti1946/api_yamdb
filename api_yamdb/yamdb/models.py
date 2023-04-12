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

    def __str__(self):
        return self.slug


class Genres(models.Model):
    name = models.CharField(max_length=256, blank=False, null=False)
    slug = models.SlugField(
        max_length=50, blank=False, null=False, unique=True
    )

    def __str__(self):
        return self.slug


class Titles(models.Model):
    name = models.CharField(
        "Название", max_length=256, blank=False, null=False
    )
    year = models.IntegerField("Год выпуска", blank=False, null=False)
    description = models.TextField("Описание", blank=True, null=True)
    genre = models.ManyToManyField(
        Genres,
        through="GenreTitle",
    )
    category = models.ForeignKey(
        Categories,
        blank=False,
        null=False,
        on_delete=models.DO_NOTHING,
        related_name="titles",
    )


class GenreTitle(models.Model):
    genre = models.ForeignKey(Genres, on_delete=models.CASCADE)
    title = models.ForeignKey(Titles, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title} {self.genre}"