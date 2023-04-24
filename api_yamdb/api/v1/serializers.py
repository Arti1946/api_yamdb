from rest_framework import serializers

import re

from django.shortcuts import get_object_or_404
from django.db.models import Avg

from datetime import datetime as dt

from reviews.models import (
    Categories,
    Genres,
    Title,
    Users,
    GenreTitle,
    Review,
    Comments,
)


class SendCodeSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True, max_length=254)
    username = serializers.RegexField(
        regex=r"^[\w.@+-]+$", max_length=150, required=True
    )

    def validate_username(self, value):
        if value == "me":
            raise serializers.ValidationError("Нельзя выбрать такое имя")
        return value


class CheckCodeSerializer(serializers.Serializer):
    username = serializers.RegexField(
        regex=r"^[\w.@+-]+$", max_length=150, required=True
    )
    confirmation_code = serializers.CharField(required=True)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("name", "slug")
        model = Categories


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("name", "slug")
        model = Genres


class TitleSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True)
    category = CategorySerializer()
    rating = serializers.SerializerMethodField()

    class Meta:
        fields = (
            "id",
            "name",
            "year",
            "description",
            "genre",
            "category",
            "rating",
        )
        model = Title

    def get_rating(self, title):
        rating = title.reviews.aggregate(Avg("score"))["score__avg"]
        return rating if rating is not None else None


class TitleSerializerPost(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        queryset=Genres.objects.all(), many=True, slug_field="slug"
    )
    category = serializers.SlugRelatedField(
        queryset=Categories.objects.all(), slug_field="slug"
    )
    rating = serializers.SerializerMethodField()

    class Meta:
        fields = (
            "id",
            "name",
            "year",
            "description",
            "genre",
            "category",
            "rating",
        )
        model = Title

    def validate_birth_year(self, value):
        year = dt.date.today().year
        if value > year:
            raise serializers.ValidationError("Проверьте год Создания!")
        return value

    def create(self, validated_data):
        genres = validated_data.pop("genre")
        title = Title.objects.create(**validated_data)
        for genre in genres:
            current_genre = get_object_or_404(Genres, slug=genre)
            GenreTitle.objects.create(genre=current_genre, title=title)
        return title

    def get_rating(self, title):
        rating = title.reviews.aggregate(Avg("score"))["score__avg"]
        return rating if rating is not None else None


class UserSerializer(serializers.ModelSerializer):
    def validate_username(self, value):
        regex = re.compile(r"^[\w.@+-]+\Z")
        if regex.match(value):
            return value
        else:
            raise serializers.ValidationError("Выберите другое имя")

    class Meta:
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "bio",
            "role",
        )
        model = Users


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field="username",
        read_only=True,
        default=serializers.CurrentUserDefault(),
    )

    class Meta:
        model = Review
        exclude = ("title",)

    def validate(self, data):
        request = self.context["request"]
        author = request.user
        title_id = self.context["view"].kwargs.get("title_id")
        title = get_object_or_404(Title, pk=title_id)
        if (
            request.method == "POST"
            and Review.objects.filter(title=title, author=author).exists()
        ):
            raise serializers.ValidationError("Ваш отзыв уже зарегистрирован")
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field="username", read_only=True
    )

    class Meta:
        model = Comments
        fields = (
            "id",
            "text",
            "author",
            "pub_date",
        )
