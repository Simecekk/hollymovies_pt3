"""
URL configuration for hollymovies project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from hollymovies_app.views import hello_world, HomepageView, AllMoviesView, MovieDetailView, CommentLikeView, \
    CommentDislikeView

urlpatterns = [
    path('admin/', admin.site.urls),
    path("hello/", hello_world),
    path("", HomepageView.as_view(), name="homepage"),
    path("movies/", AllMoviesView.as_view(), name="all_movies"),
    path("movie/<int:movie_id>/", MovieDetailView.as_view(), name="movie_detail"),
    path("movie/comment/like/<int:comment_id>/", CommentLikeView.as_view(), name="movie_comment_like"),
    path("movie/comment/dislike/<int:comment_id>", CommentDislikeView.as_view(), name="movie_comment_dislike")
]
