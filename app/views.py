from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import MoviePerson, Movie, Review
from .forms import MovieForm, ReviewForm, MoviePersonForm


def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def movies_list(request):
    movies = Movie.objects.all()
    list = {
        'contents': movies,
        'type': 'movie',
        'url': 'movie',
        'create_form': 'movie-create-form',
        'update_form': 'update-movie-form',
        'delete_form': 'delete-movie-form',
    }
    return render(request, 'lists.html', {'list': list})	

def actors_list(request):
    actors = MoviePerson.objects.filter(actor=True)
    list = {
        'contents': actors,
        'type': 'actor',
        'url': 'movie_person',    
        'create_form': 'movie_person-create-form',
        'update_form': 'update-movie_person-form',
        'delete_form': 'delete-movie_person-form',
    }
    return render(request, 'lists.html', {'list': list})

def directors_list(request):
    directors = MoviePerson.objects.filter(director=True)
    list = {
        'contents': directors,
        'type': 'dirrector',
        'url': 'movie_person',
        'create_form': 'movie_person-create-form',
        'update_form': 'update-movie_person-form',
        'delete_form': 'delete-movie_person-form',
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
     error = None

     if request.method == 'POST':
        username = request.POST.get('username').lower()
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_again = request.POST.get('password-again')
        
        #daco s emailom

        if password != password_again:
            error = "Passwords do not match"
            return render(request, 'register_page.html', {'error': error})
        
        if User.objects.filter(username=username).exists():
            error = "Username is already taken"
            return render(request, 'register_page.html', {'error': error})
        
        user = User.objects.create_user(username=username, password=password, email=email)
        return redirect('login')
     return render(request, 'register_page.html', {'error': error})

def movie(request, pk):
    movie = Movie.objects.get(id=pk)
    reviews = Movie.objects.get(id=pk).reviews.all()
    list = {
        'movie': movie,
        'reviews': reviews,
    }
    return render(request, 'movie.html', {'list': list})

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

def createMovie(request):
    form = MovieForm()
    if request.method == 'POST':
        form = MovieForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('movies_list')             
    return render(request, 'movie_create_form.html', {'form': form})


def updateMovie(request, pk):
    movie = Movie.objects.get(id=pk)
    form = MovieForm(instance=movie)
    if request.method == 'POST':
        form = MovieForm(request.POST, instance=movie)
        if form.is_valid():
             form.save()
             return redirect('movies_list')
    return render(request, 'movie_create_form.html', {'form': form})

def deleteMovie(request, pk):
     movie = Movie.objects.get(id=pk)
     if request.method == 'POST':
          movie.delete()
          return redirect('movies_list')
     return render(request, 'delete.html', {'obj':movie})
    
def createMoviePersonForm(request):
    form = MoviePersonForm()
    if request.method == 'POST':
            form = MoviePersonForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('actors_list')             
    return render(request, 'movie_person_create_form.html', {'form': form})
   
def updateMoviePerson(request, pk):
    moviePerson = MoviePerson.objects.get(id=pk)
    form = MoviePersonForm(instance=moviePerson)
    if request.method == 'POST':
        form = MoviePersonForm(request.POST, instance=moviePerson)
        if form.is_valid():
             form.save()
             return redirect('actors_list')
    return render(request, 'movie_person_create_form.html', {'form': form})

def deleteMoviePerson(request, pk):
    moviePerson = MoviePerson.objects.get(id=pk)
    if request.method == 'POST':
        moviePerson.delete()
        return redirect('actors_list')
    return render(request, 'delete.html', {'obj':moviePerson})

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

def updateReview(request, pk):
    review = Review.objects.get(id=pk)
    form = ReviewForm(instance=review)
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return redirect('movie', pk=review.movie.id)
    return render(request, 'review_create_form.html', {'form': form, 'review': review})

def deleteReview(request, pk):
    review = Review.objects.get(id=pk)
    if request.method == 'POST':
        review.delete()
        return redirect('movie', pk=review.movie.id)
    return render(request, 'delete.html', {'obj': review})

