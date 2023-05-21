from django.http import HttpResponse
from django.template.response import TemplateResponse
from hollymovies_app.models import Movie


def homepage(request):
    context = {
        "title": "Homepage"
    }
    return TemplateResponse(request, "homepage.html", context=context)


def all_movies(request):
    context = {
        "best_movies": Movie.objects.filter(rating__gte=5).order_by("-rating"),
        "worst_movies": Movie.objects.filter(rating__lt=5).order_by("rating"),
        "movies_count": Movie.objects.all().count(),
    }
    return TemplateResponse(request, "movies.html", context=context)


def movie_detail(request, movie_id):
    context = {
        "movie": Movie.objects.get(id=movie_id)
    }
    return TemplateResponse(request, "movie_detail.html", context=context)


def hello_world(request):
    name = request.GET.get("name", "DEFAULT")
    return HttpResponse(f"Hello world {name}")
