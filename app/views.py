from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import MoviePerson, Movie, Review
from .forms import MovieForm, RegistrationForm, ReviewForm, MoviePersonForm
from django.http import JsonResponse
from django.urls import reverse

def moderator_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden("You don't have permission to access this page")
        if not (request.user.groups.filter(name="Moderator").exists() or request.user.is_superuser):
            return HttpResponseForbidden("You don't have permission to access this page")
        return view_func(request, *args, **kwargs)
    return wrapper


def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def movies_list(request):
    movies = Movie.objects.all()
    permission = request.user.is_authenticated and (request.user.groups.filter(name="Moderator").exists() or request.user.is_superuser)
    list = {
        'contents': movies,
        'type': 'movie',
        'url': 'movie',
        'create_form': 'movie-create-form',
        'update_form': 'update-movie-form',
        'delete_form': 'delete-movie-form',
        'permission': permission,
    }
    return render(request, 'lists.html', {'list': list})	

def actors_list(request):
    actors = MoviePerson.objects.filter(actor=True)
    permission = request.user.is_authenticated and (request.user.groups.filter(name="Moderator").exists() or request.user.is_superuser)
    list = {
        'contents': actors,
        'type': 'actor',
        'url': 'movie_person',    
        'create_form': 'movie_person-create-form',
        'update_form': 'update-movie_person-form',
        'delete_form': 'delete-movie_person-form',
        'permission': permission,
    }
    return render(request, 'lists.html', {'list': list})

def directors_list(request):
    directors = MoviePerson.objects.filter(director=True)
    permission = request.user.is_authenticated and (request.user.groups.filter(name="Moderator").exists() or request.user.is_superuser)
    list = {
        'contents': directors,
        'type': 'dirrector',
        'url': 'movie_person',
        'create_form': 'movie_person-create-form',
        'update_form': 'update-movie_person-form',
        'delete_form': 'delete-movie_person-form',
        'permission': permission,
    }
    return render(request, 'lists.html', {'list': list})

def login_page(request):
    error = None
    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            error = "Username or password is incorrect"
            
    return render(request, 'login_page.html', {'error': error})

def logout_user(request):
     logout(request)
     return redirect('index')

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username').lower()
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            User.objects.create_user(username=username, email=email, password=password)
            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, 'register_page.html', {'form': form})

def movie(request, pk):
    movie = Movie.objects.get(id=pk)
    reviews = Movie.objects.get(id=pk).reviews.all()
    permission = request.user.is_authenticated and (request.user.groups.filter(name="Moderator").exists() or request.user.is_superuser or request.user.groups.filter(name="Reviewer").exists())
    list = {
        'movie': movie,
        'reviews': reviews,
        'permission': permission,
    }
    return render(request, 'movie.html', {'list': list})

def get_reviews(request, pk):
    reviews = Movie.objects.get(id=pk).reviews.all()
    review_list = []
    for review in reviews:
        permission = request.user.is_authenticated and (request.user.groups.filter(name="Moderator").exists() or
                     request.user.is_superuser or request.user.groups.filter(name="Reviewer").exists() or
                     request.user == review.user)
        review_list.append({
            'user': review.user.username,
            'rating': review.rating,
            'comment': review.comment,
            'permission': permission,
            'update_url': reverse('update-review-form', kwargs={'pk': review.id}),
            'delete_url': reverse('delete-review-form', kwargs={'pk': review.id}),
        })
    return JsonResponse({'reviews': review_list})


def movie_person(request, pk):
    person = MoviePerson.objects.get(id=pk)
    movies_played_in = Movie.objects.filter(actors=person)
    movies_directed = Movie.objects.filter(director=person)
    list = {
        'person': person,
        'movies_played_in': movies_played_in,
        'movies_directed': movies_directed,
    }
    return render(request, 'movie_person.html', {'list': list})

@moderator_required
def createMovie(request):
    form = MovieForm()
    if request.method == 'POST':
        form = MovieForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('movies_list')             
    return render(request, 'movie_create_form.html', {'form': form})

@moderator_required
def updateMovie(request, pk):
    movie = Movie.objects.get(id=pk)
    form = MovieForm(instance=movie)
    if request.method == 'POST':
        form = MovieForm(request.POST, request.FILES, instance=movie)
        if form.is_valid():
             form.save()
             return redirect('movies_list')
    return render(request, 'movie_create_form.html', {'form': form})

@moderator_required
def deleteMovie(request, pk):
     movie = Movie.objects.get(id=pk)
     if request.method == 'POST':
          movie.delete()
          return redirect('movies_list')
     return render(request, 'delete.html', {'obj':movie})
    
@moderator_required
def createMoviePersonForm(request):
    form = MoviePersonForm()
    if request.method == 'POST':
            form = MoviePersonForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('actors_list')             
    return render(request, 'movie_person_create_form.html', {'form': form})

@moderator_required  
def updateMoviePerson(request, pk):
    moviePerson = MoviePerson.objects.get(id=pk)
    form = MoviePersonForm(instance=moviePerson)
    if request.method == 'POST':
        form = MoviePersonForm(request.POST, instance=moviePerson)
        if form.is_valid():
             form.save()
             return redirect('actors_list')
    return render(request, 'movie_person_create_form.html', {'form': form})

@moderator_required
def deleteMoviePerson(request, pk):
    moviePerson = MoviePerson.objects.get(id=pk)
    if request.method == 'POST':
        moviePerson.delete()
        return redirect('actors_list')
    return render(request, 'delete.html', {'obj':moviePerson})

@login_required
def createReview(request, pk):
    form = ReviewForm()
    movie = Movie.objects.get(id=pk)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            try:
                review = form.save(commit=False)
                review.movie = movie
                review.user = request.user
                review.save()
                return redirect('movie', pk=pk)
            except:
                form.add_error(None, 'You have already submited a review for this movie')
    return render(request, 'review_create_form.html', {'form': form, 'movie': movie})

@login_required
def updateReview(request, pk):
    review = Review.objects.get(id=pk)
    if request.user != review.user and not (request.user.groups.filter(name="Moderator").exists() or request.user.is_superuser or request.user.groups.filter(name="Reviewer").exists()):
        return HttpResponseForbidden("You don't have permission to access this page")
    
    form = ReviewForm(instance=review)
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return redirect('movie', pk=review.movie.id)
    return render(request, 'review_create_form.html', {'form': form, 'review': review})

@login_required
def deleteReview(request, pk):
    review = Review.objects.get(id=pk)
    if request.user != review.user and not (request.user.groups.filter(name="Moderator").exists() or request.user.is_superuser or request.user.groups.filter(name="Reviewer").exists()):
        return HttpResponseForbidden("You don't have permission to access this page")
    
    if request.method == 'POST':
        review.delete()
        return redirect('movie', pk=review.movie.id)
    return render(request, 'delete.html', {'obj': review})

