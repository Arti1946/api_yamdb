import csv

from django.core.management.base import BaseCommand

from yamdb.models import Categories, Genres, GenreTitle, Titles, Users


def category(file):
    input_file = csv.DictReader(open(file, encoding="utf8"))
    for row in input_file:
        Categories.objects.create(
            id=row["id"], slug=row["slug"], name=row["name"]
        )


def genre(file):
    input_file = csv.DictReader(open(file, encoding="utf8"))
    for row in input_file:
        Genres.objects.create(id=row["id"], slug=row["slug"], name=row["name"])


def genre_title(file):
    input_file = csv.DictReader(open(file, encoding="utf8"))
    for row in input_file:
        GenreTitle.objects.create(
            id=row["id"], title_id=row["title_id"], genre_id=row["genre_id"]
        )


def titles(file):
    input_file = csv.DictReader(open(file, encoding="utf8"))
    for row in input_file:
        cate = Categories.objects.get(id=row["category"])
        Titles.objects.create(
            id=row["id"],
            name=row["name"],
            year=row["year"],
            category=cate,
        )


def users(file):
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


class Command(BaseCommand):
    def handle(self, *args, **options):
        genre("static/data/genre.csv")
        category("static/data/category.csv")
        titles("static/data/titles.csv")
        genre_title("static/data/genre_title.csv")
        users("static/data/users.csv")
