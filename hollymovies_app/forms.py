from django import forms
from django.core.exceptions import ValidationError
from hollymovies_app.models import Comment


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
