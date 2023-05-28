from django.contrib import admin
from hollymovies_app.models import Country, Movie, Actor, Comment, Contact


class MovieAdmin(admin.ModelAdmin):
    list_display = ["name", "genre", "country", "id"]


class CountryAdmin(admin.ModelAdmin):
    list_display = ["name", "id"]


class ActorAdmin(admin.ModelAdmin):
    list_display = ["name", "age", "gender", "country", "id"]


class CommentAdmin(admin.ModelAdmin):
    list_display = ["text", "id", "username", "likes"]


class ContactAdmin(admin.ModelAdmin):
    list_display = ["email", "id", "name", "text", "priority"]


admin.site.register(Movie, MovieAdmin)
admin.site.register(Country, CountryAdmin)
admin.site.register(Actor, ActorAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Contact, ContactAdmin)
