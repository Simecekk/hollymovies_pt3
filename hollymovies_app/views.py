from django.http import HttpResponse
from django.template.response import TemplateResponse
from hollymovies_app.models import Movie
from django.views import View
from django.views.generic import TemplateView


class HomepageView(TemplateView):
    template_name = "homepage.html"
    extra_context = {"title": "Homepage"}


class AllMoviesView(View):
    # Restrict only GET method
    http_method_names = ["get", ]

    def get(self, request, *args, **kwargs):
        context = {
            "best_movies": Movie.objects.filter(rating__gte=5).order_by("-rating"),
            "worst_movies": Movie.objects.filter(rating__lt=5).order_by("rating"),
            "movies_count": Movie.objects.all().count(),
        }
        return TemplateResponse(request, "movies.html", context=context)


class MovieDetailView(View):
    def get(self, request, movie_id, *args, **kwargs):
        context = {
            "movie": Movie.objects.get(id=movie_id)
        }
        return TemplateResponse(request, "movie_detail.html", context=context)


def hello_world(request):
    name = request.GET.get("name", "DEFAULT")
    return HttpResponse(f"Hello world {name}")
