from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from hollymovies_app.models import Comment, CinemaTicket


class BadWordCharField(forms.CharField):
    def validate(self, value):
        bad_words = ["zakazene", "david", "chatgpt"]

        for bad_word in bad_words:
            if bad_word in value:
                raise ValidationError("Text cannot contains zakazane slovo")

        return value


class ContactForm(forms.Form):
    name = forms.CharField(max_length=50)
    email = forms.EmailField()
    text = BadWordCharField(widget=forms.Textarea(attrs={"class": "form-control"}))
    priority = forms.IntegerField(min_value=1, max_value=10)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["username", "text"]


class CinemaTicketForm(forms.ModelForm):

    class Meta:
        model = CinemaTicket
        fields = ["buyer_name", "quantity"]

    def __init__(self, screening=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.screening = screening
        self.fields["quantity"] = forms.IntegerField(
            widget=forms.NumberInput(attrs={"onchange": "calculateTotalPrice()"}),
            max_value=screening.available_tickets,
            min_value=1,
        )

    def clean_quantity(self):
        value = int(self.data["quantity"])
        if value > self.screening.available_tickets:
            raise ValidationError(f"Error: Max available tickets: {self.screening.available_tickets}")
        return value


class RegistrationForm(UserCreationForm):
    error_messages = {
        "password_mismatch": "Špatně zadané heslo",
    }

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

