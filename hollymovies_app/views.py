from django.http import HttpResponse
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from hollymovies_app.models import Movie, Comment, Contact
from django.views import View
from django.views.generic import TemplateView
from hollymovies_app.forms import ContactForm


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


class ContactView(View):

    def get(self, request, *args, **kwargs):
        # generate form in template
        context = {
            "contact_form": ContactForm()
        }
        return TemplateResponse(request, "contact.html", context=context)

    def post(self, request, *args, **kwargs):
        # validate submited form
        data = request.POST
        bounded_form = ContactForm(data=data)

        if bounded_form.is_valid():
            Contact.objects.create(
                text=bounded_form.cleaned_data["text"],
                email=bounded_form.cleaned_data["email"],
                name=bounded_form.cleaned_data["name"],
                priority=bounded_form.cleaned_data["priority"]
            )
            return redirect("success_contact")

        return TemplateResponse(request, "contact.html", context={"contact_form": bounded_form})


class SuccessContactView(TemplateView):
    template_name = "success_contact.html"
