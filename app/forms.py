import re
from django import forms
from django.contrib.auth.models import User
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

        widgets = { 
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'picture': forms.URLInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'birth_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'director': forms.CheckboxInput(attrs={'class': 'form-check-input'}),	
            'actor': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        
class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']

        widgets = {
            'rating': forms.NumberInput(attrs={'class': 'form-control'}),
            'comment': forms.Textarea(attrs={'class': 'form-control'}),
        }


class RegistrationForm(forms.Form):
    username = forms.CharField(max_length=100)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())
    password_again = forms.CharField(widget=forms.PasswordInput())

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('This username is already taken')
        return username
    
    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 8:
            raise forms.ValidationError('Password must be at least 8 characters long')
        if not re.search(r"[A-Z]", password):
            raise forms.ValidationError('Password must contain at least one upercase character')
        if not re.search(r"\d", password):
            raise forms.ValidationError('Password must contain at least one number')
        return password

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_again = cleaned_data.get('password_again')
        if password != password_again:
            self.add_error('password_again', 'Passwords do not match')
        return cleaned_data