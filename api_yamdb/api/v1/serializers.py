from rest_framework import serializers

from django.shortcuts import get_object_or_404

from reviews.models import (
    Categories, Comments, Genres, GenreTitle, Review, Title, Users,
)


class SendCodeSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True, max_length=254)
    username = serializers.CharField(max_length=150, required=True)


class CheckCodeSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150, required=True)
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
    rating = serializers.IntegerField(read_only=True)

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


class TitleSerializerPost(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        queryset=Genres.objects.all(), many=True, slug_field="slug"
    )
    category = serializers.SlugRelatedField(
        queryset=Categories.objects.all(), slug_field="slug"
    )
    rating = serializers.IntegerField(read_only=True)

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

    def create(self, validated_data):
        genres = validated_data.pop("genre")
        title = Title.objects.create(**validated_data)
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
