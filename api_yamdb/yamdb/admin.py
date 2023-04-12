from django.contrib import admin

from yamdb.models import Users, Titles, Genres, Categories, GenreTitle

admin.site.register(Users)
admin.site.register(Titles)
admin.site.register(Genres)
admin.site.register(Categories)
admin.site.register(GenreTitle)
