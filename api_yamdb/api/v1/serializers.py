from rest_framework import serializers

from datetime import datetime as dt

from yamdb.models import Categories, Genres, Titles, Users


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("name", "slug")
        model = Categories


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("name", "slug")
        model = Genres


class TitleSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("name", "year", "description", "genre", "category")
        model = Titles

    def validate_birth_year(self, value):
        year = dt.date.today().year
        if value > year:
            raise serializers.ValidationError("Проверьте год Создания!")
        return value


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
