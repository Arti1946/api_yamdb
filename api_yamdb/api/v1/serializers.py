from rest_framework import serializers

from django.shortcuts import get_object_or_404

from datetime import datetime as dt

from yamdb.models import Categories, Genres, Titles, Users, GenreTitle


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
    category = serializers.SlugRelatedField(
        slug_field="slug",
        queryset=Categories.objects.all(),
    )

    class Meta:
        fields = ("id", "name", "year", "description", "genre", "category")
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


class UserSerializer(serializers.ModelSerializer):
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
