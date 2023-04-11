from django.contrib import admin

from yamdb.models import Users, Titles, Genres, Categories

admin.site.register(Users)
admin.site.register(Titles)
admin.site.register(Genres)
admin.site.register(Categories)
