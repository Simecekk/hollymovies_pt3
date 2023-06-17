from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.views.generic.edit import FormMixin

from hollymovies_app.models import Movie, Comment, Contact, Cinema, CinemaScreening, CinemaTicket
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView
from hollymovies_app.forms import ContactForm, CommentForm, CinemaTicketForm, RegistrationForm


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
            "comments": movie.comments.all().order_by("-likes"),
            "comment_form": CommentForm()
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


class AddCommentView(View):

    def post(self, request, movie_id, *args, **kwargs):
        movie = Movie.objects.get(id=movie_id)
        bounded_form = CommentForm(data=request.POST)
        if bounded_form.is_valid():
            Comment.objects.create(
                username=bounded_form.cleaned_data["username"],
                movie=movie,
                text=bounded_form.cleaned_data["text"]
            )

        return redirect("movie_detail", movie_id=movie_id)


class CinemaListView(ListView):
    model = Cinema
    template_name = "cinema_list.html"


class CinemaDetailView(DetailView):
    model = Cinema
    template_name = "cinema_detail.html"


class TicketBuyView(View):

    def get(self, request, screening_id, *args, **kwargs):
        # generate form in template
        screening = CinemaScreening.objects.get(id=screening_id)
        context = {
            "ticket_form": CinemaTicketForm(screening=screening),
            "screening": screening
        }
        return TemplateResponse(request, "ticket_buy.html", context=context)

    def post(self, request, screening_id, *args, **kwargs):
        screening = CinemaScreening.objects.get(id=screening_id)
        bounded_form = CinemaTicketForm(data=request.POST, screening=screening)

        if bounded_form.is_valid():
            CinemaTicket.objects.create(
                buyer_name=bounded_form.cleaned_data["buyer_name"],
                quantity=bounded_form.cleaned_data["quantity"],
                screening=screening
            )
            return redirect("cinema_detail", pk=screening.cinema.id)
        else:
            context = {
                "ticket_form": bounded_form,
                "screening": screening
            }
            return TemplateResponse(request, "ticket_buy.html", context=context)


class LoginView(FormMixin, TemplateView):
    """
    NOTE: Django has built it LoginView (from django.contrib.auth.views import LoginView).

    Reason why I'm not using it is that I wanted to explain how is it done under the hood
    """
    template_name = 'login.html'
    form_class = AuthenticationForm

    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('homepage')

        return redirect('login')


class LogoutView(View):
    """
    NOTE: Django has built it LogoutView (from django.contrib.auth.views import LogoutView)
    but this django LogoutView expect us to have logout template.

    In our case we will have LogoutView in the base template. So we implement it ourselves.
    """
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('homepage')


class RegistrationView(FormMixin, TemplateView):
    template_name = 'registration.html'
    form_class = RegistrationForm

    def post(self, request,  *args, **kwargs):
        registration_data = request.POST
        form = self.form_class(registration_data)
        if form.is_valid():
            form.save()
            return redirect('login')
        else:
            return TemplateResponse(request, 'registration.html', context={'form': form})
