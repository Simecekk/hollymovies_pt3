from django.contrib import admin
from hollymovies_app.models import Country, Movie, Actor


class MovieAdmin(admin.ModelAdmin):
    list_display = ["name", "genre", "country", "id"]


class CountryAdmin(admin.ModelAdmin):
    list_display = ["name", "id"]


class ActorAdmin(admin.ModelAdmin):
    list_display = ["name", "age", "gender", "country", "id"]


admin.site.register(Movie, MovieAdmin)
admin.site.register(Country, CountryAdmin)
admin.site.register(Actor, ActorAdmin)
