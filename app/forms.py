from datetime import timezone
from django.utils import timezone
from datetime import date
import re
from urllib.request import urlopen
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

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'picture': forms.FileInput(attrs={'class': 'form-control'}),
            'genre': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'release_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'length': forms.NumberInput(attrs={'class': 'form-control'}),
            'director': forms.Select(attrs={'class': 'form-control'}),
            'actors': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(MovieForm, self).__init__(*args, **kwargs)
        self.fields['director'].queryset = MoviePerson.objects.filter(director=True).order_by('name')
        self.fields['actors'].queryset = MoviePerson.objects.filter(actor=True).order_by('name')
            
    def clean_name(self):
        name = self.cleaned_data.get('name')
        if not name.strip():
            raise forms.ValidationError('Name cannot be empty')
        if len(name) < 2:
            raise forms.ValidationError('Name must be at least 2 characters long')
        return name
    
    def clean_picture(self):
        picture = self.cleaned_data.get('picture')
        if picture.size > 5 * 1024 * 1024:
            raise forms.ValidationError('Image file cannot be larger than 5MB')
        
        valid_formats = ['.jpg', '.png', '.jpeg']
        format = picture.name.split('.')[-1]
        if f'.{format}' not in valid_formats:
            raise forms.ValidationError('Invalid file format')
        return picture
    
    def clean_description(self):
        description = self.cleaned_data.get('description')
        if not description.strip():
            raise forms.ValidationError('Description cannot be empty')
        return description
    
    def clean_release_date(self):
        release_date = self.cleaned_data.get('release_date')
        if release_date > timezone.now().date():
            raise forms.ValidationError('Invalid date')
        return release_date
    
    def clean_length(self):
        length = self.cleaned_data.get('length')
        if length and length < 1:
            raise forms.ValidationError('Length must be at least 1 minute')
        if length and length > 1000:
            raise forms.ValidationError('Length must be at most 1000 minutes')
        return length
    
    def clean(self):
        return self.cleaned_data



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
        
    def clean_name(self):
        name = self.cleaned_data.get('name')
        if not name.strip():
            raise forms.ValidationError('Name cannot be empty')
        return name
        
    def clean_picture(self):
        picture = self.cleaned_data.get('picture')

        if picture:
            try:
                with urlopen(picture, timeout=5) as response:
                    content = response.headers.get('Content-Type')
                
                    if not content.startswith('image/'):
                        raise forms.ValidationError('This is not a picture URL')
            
            except:
                raise forms.ValidationError('There is some problem with the URL')

        return picture
        
    def clean_description(self):
        description = self.cleaned_data.get('description')
        if not description.strip():
            raise forms.ValidationError('Description cannot be empty')
        return description

    def clean_birth_date(self):
        birth_date = self.cleaned_data.get('birth_date')
        if birth_date and birth_date > date.today():
            raise forms.ValidationError('Invalid birth date')
        return birth_date
    
    def clean(self):
        cleaned_data = super().clean()
        director = cleaned_data.get('director')
        actor = cleaned_data.get('actor')

        if not director and not actor:
            raise forms.ValidationError('Person must be a director or an actor')
        return cleaned_data

class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']

        widgets = {
            'rating': forms.NumberInput(attrs={'class': 'form-control'}),
            'comment': forms.Textarea(attrs={'class': 'form-control'}),
        }

    def clean_rating(self):
        rating = self.cleaned_data.get('rating')
        if rating < 0 or rating > 100:
            raise forms.ValidationError('The value must be between 0 and 100')
        return rating
    
    def clean(self):
        return self.cleaned_data


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
        if password and password_again and password != password_again:
            self.add_error('password_again', 'Passwords do not match')
        return cleaned_data