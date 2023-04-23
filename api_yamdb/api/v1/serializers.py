from rest_framework import serializers

import re

from django.shortcuts import get_object_or_404
from django.db.models import Avg

from datetime import datetime as dt

from yamdb.models import Categories, Genres, Titles, Users, GenreTitle, Reviews, Comments


class SendCodeSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True, max_length=254)
    username = serializers.RegexField(
        regex=r'^[\w.@+-]+$',
        max_length=150,
        required=True
    )

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                "Нельзя выбрать такое имя")
        return value


class CheckCodeSerializer(serializers.Serializer):
    username = serializers.RegexField(
        regex=r'^[\w.@+-]+$',
        max_length=150,
        required=True
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
    genre = serializers.SlugRelatedField(
        slug_field="slug", queryset=Genres.objects.all(), many=True
    )
    category = serializers.SlugRelatedField(slug_field="slug", queryset=Categories.objects.all())
    rating = serializers.SerializerMethodField()

    class Meta:
        fields = ("id", "name", "year", "description", "genre", "category", "rating")
        model = Titles

    def validate_birth_year(self, value):
        year = dt.date.today().year
        if value > year:
            raise serializers.ValidationError("Проверьте год Создания!")
        return value

    def create(self, validated_data):
        genres = validated_data.pop("genre")
        title = Titles.objects.create(**validated_data)
        for genre in genres:
            current_genre = get_object_or_404(Genres, slug=genre)
            GenreTitle.objects.create(genre=current_genre, title=title)
        return title

    def get_rating(self, title):
        rating = title.reviews.aggregate(Avg('score'))['score__avg']
        return rating if rating is not None else None


class UserSerializer(serializers.ModelSerializer):
    def validate_username(self, value):
        regex = re.compile(r'^[\w.@+-]+\Z')
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
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Reviews
        fields = (
            "id",
            "text",
            "author",
            "score",
            "pub_date",
        )


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Comments
        fields = (
            "review",
            "text",
            "author",
            "pub_date",
        )