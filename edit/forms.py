from django import forms
from movieapp.models import Movie,Category


class MovieForm(forms.ModelForm):
    class Meta:
        model=Movie
        fields=['title','actor','desc','release','poster','category','link']

