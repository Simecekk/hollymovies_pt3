from django.http import HttpResponse
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from hollymovies_app.models import Movie, Comment
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


class CommentLikeView(View):

    def post(self, request, comment_id, *args, **kwargs):
        comment = Comment.objects.get(id=comment_id)
        comment.likes += 1
        comment.save()
        return redirect("movie_detail", movie_id=comment.movie.id)


class CommentDislikeView(View):

    def post(self, request, comment_id, *args, **kwargs):
        comment = Comment.objects.get(id=comment_id)
        comment.likes -= 1
        comment.save()
        return redirect("movie_detail", movie_id=comment.movie.id)


class MovieDetailView(View):
    def get(self, request, movie_id, *args, **kwargs):
        movie = Movie.objects.get(id=movie_id)
        context = {
            "movie": movie,
            "comments": movie.comments.all().order_by("-likes")
        }
        return TemplateResponse(request, "movie_detail.html", context=context)


def hello_world(request):
    name = request.GET.get("name", "DEFAULT")
    return HttpResponse(f"Hello world {name}")
