from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Country(models.Model):
    name = models.CharField(max_length=200)

    class Meta:
        verbose_name_plural = "Countries"

    def __str__(self):
        return self.name


class Actor(models.Model):
    GENDER_MALE = "male"
    GENDER_FEMALE = "female"

    GENDER_CHOICES = (
        (GENDER_FEMALE, "female"),
        (GENDER_MALE, "male")
    )

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, default="")
    age = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(120)])
    country = models.ForeignKey(Country, on_delete=models.PROTECT, related_name="actors")
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default=GENDER_MALE)

    def __str__(self):
        return self.name


class Movie(models.Model):
    GENRE_HORROR = "hrh"
    GENRE_COMEDY = "cmd"
    GENRE_ACTION = "ac"
    GENRE_DRAMA = "dr"

    GENRE_CHOICES = (
        (GENRE_HORROR, "horror"),
        (GENRE_COMEDY, "comedy"),
        (GENRE_ACTION, "action"),
        (GENRE_DRAMA, "drama")
    )

    name = models.CharField(max_length=50)
    description = models.TextField(blank=True, default="")
    rating = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)])
    release_date = models.DateField()
    genre = models.CharField(choices=GENRE_CHOICES, max_length=20, default=GENRE_COMEDY)
    country = models.ForeignKey(Country, on_delete=models.PROTECT, related_name="movies")
    actors = models.ManyToManyField(Actor, related_name="movies")

    def __str__(self):
        return self.name


class Comment(models.Model):
    text = models.TextField()
    likes = models.IntegerField(default=0)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="comments")
    username = models.CharField(max_length=30)


class Contact(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()
    text = models.TextField()
    priority = models.IntegerField()
