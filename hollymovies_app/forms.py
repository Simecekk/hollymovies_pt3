from django import forms


class ContactForm(forms.Form):
    name = forms.CharField(max_length=50)
    email = forms.EmailField()
    text = forms.CharField(widget=forms.Textarea(attrs={"class": "form-control"}))
    priority = forms.IntegerField()
