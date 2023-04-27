import csv

from django.core.management.base import BaseCommand

from reviews.models import (
    Categories, Comments, Genres, GenreTitle, Review, Title, Users,
)


def category(file: str) -> None:
    input_file = csv.DictReader(open(file, encoding="utf8"))
    for row in input_file:
        Categories.objects.create(
            id=row["id"], slug=row["slug"], name=row["name"]
        )


def genre(file: str) -> None:
    input_file = csv.DictReader(open(file, encoding="utf8"))
    for row in input_file:
        Genres.objects.create(id=row["id"], slug=row["slug"], name=row["name"])


def genre_title(file: str) -> None:
    input_file = csv.DictReader(open(file, encoding="utf8"))
    for row in input_file:
        GenreTitle.objects.create(
            id=row["id"], title_id=row["title_id"], genre_id=row["genre_id"]
        )


def titles(file: str) -> None:
    input_file = csv.DictReader(open(file, encoding="utf8"))
    for row in input_file:
        cate = Categories.objects.get(id=row["category"])
        Title.objects.create(
            id=row["id"],
            name=row["name"],
            year=row["year"],
            category=cate,
        )


def users(file: str) -> None:
    input_file = csv.DictReader(open(file, encoding="utf8"))
    for row in input_file:
        Users.objects.create(
            id=row["id"],
            username=row["username"],
            email=row["email"],
            role=row["role"],
            bio=row["bio"],
            first_name=row["first_name"],
            last_name=row["last_name"],
        )


def comments(file: str) -> None:
    input_file = csv.DictReader(open(file, encoding="utf8"))
    for row in input_file:
        author = Users.objects.get(id=row["author"])
        Comments.objects.create(
            id=row["id"],
            review_id=row["review_id"],
            text=row["text"],
            author=author,
            pub_date=row["pub_date"],
        )


def review(file: str) -> None:
    input_file = csv.DictReader(open(file, encoding="utf8"))
    for row in input_file:
        author = Users.objects.get(id=row["author"])
        Review.objects.create(
            id=row["id"],
            title_id=row["title_id"],
            text=row["text"],
            author=author,
            score=row["score"],
            pub_date=row["pub_date"],
        )


class Command(BaseCommand):
    def handle(self, *args, **options):
        genre("static/data/genre.csv")
        category("static/data/category.csv")
        titles("static/data/titles.csv")
        genre_title("static/data/genre_title.csv")
        users("static/data/users.csv")
        review("static/data/review.csv")
        comments("static/data/comments.csv")
