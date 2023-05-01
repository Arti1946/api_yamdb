import datetime
import re

from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


def validate_username(value):
    if value == "me":
        raise ValidationError("Нельзя выбрать такое имя")
    return value


class Users(AbstractUser):
    class Roles(models.TextChoices):
        USER = "user", _("Пользователь")
        MODERATOR = "moderator", _("Модератор")
        ADMIN = (
            "admin",
            _("Администратор"),
        )

    bio = models.TextField("Биография", blank=True)
    role = models.CharField(
        verbose_name="Роль",
        max_length=9,
        choices=Roles.choices,
        default=Roles.USER,
    )
    email = models.EmailField(unique=True, max_length=254, null=False)
    username = models.CharField(max_length=150, unique=True, null=False, validators=[RegexValidator(regex=r"^[\w.@+-]+$"), validate_username])


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


class Title(models.Model):
    def validate_year(value):
        year = datetime.date.today().year
        if value > year:
            raise ValidationError("Проверьте год Создания!")

    name = models.CharField(
        "Название", max_length=256, blank=False, null=False
    )
    year = models.IntegerField(
        "Год выпуска", blank=False, null=False, validators=[validate_year]
    )
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
    title = models.ForeignKey(Title, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title} {self.genre}"


class Review(models.Model):
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name="reviews"
    )
    text = models.TextField("Текст")
    author = models.ForeignKey(
        Users, on_delete=models.CASCADE, related_name="reviews"
    )
    score = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        blank=False,
    )
    pub_date = models.DateTimeField("Дата публикации", auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["title", "author"], name="uq_title_author"
            )
        ]


class Comments(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    text = models.TextField("Текст")
    author = models.ForeignKey(
        Users, on_delete=models.CASCADE, verbose_name="comments"
    )
    pub_date = models.DateTimeField("Дата публикации", auto_now_add=True)
