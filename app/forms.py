from django.forms import ModelForm
from .models import Movie

class MovieReviewForm(ModelForm):
    class Meta:
        model = Movie
        fields = '__all__'