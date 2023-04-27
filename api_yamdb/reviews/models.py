import datetime
import re

from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _


class Users(AbstractUser):
    def validate_username(value):
        regex = re.compile(r"^[\w.@+-]+\Z")
        if not regex.match(value):
            raise ValidationError("Выберите другое имя")
        elif value == "me":
            raise ValidationError("Нельзя выбрать такое имя")

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
    email = models.EmailField(unique=True, max_length=254)
    username = models.CharField(
        "Имя пользователя",
        max_length=150,
        unique=True,
        validators=[validate_username],
    )


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
    score = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 11)])
    pub_date = models.DateTimeField("Дата публикации", auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["title", "author"], name="unique_review"
            )
        ]


class Comments(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    text = models.TextField("Текст")
    author = models.ForeignKey(
        Users, on_delete=models.CASCADE, verbose_name="comments"
    )
    pub_date = models.DateTimeField("Дата публикации", auto_now_add=True)
