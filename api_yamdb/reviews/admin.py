from django.contrib import admin

from reviews.models import Categories, Genres, GenreTitle, Title, Users

admin.site.register(Users)
admin.site.register(Title)
admin.site.register(Genres)
admin.site.register(Categories)
admin.site.register(GenreTitle)
