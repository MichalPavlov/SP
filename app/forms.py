from django.forms import ModelForm
from .models import Movie
from .models import MoviePerson
from .models import Review

class MovieForm(ModelForm):
    class Meta:
        model = Movie
        fields = '__all__'

class MoviePersonForm(ModelForm):
    class Meta:
        model = MoviePerson
        fields = '__all__'

class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']