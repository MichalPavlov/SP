from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import MoviePerson, Movie
from .forms import MovieForm
from .forms import MoviePersonForm


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
        'url': 'movie_star',    
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
        'url': 'movie_star',
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
     return render(request, 'movie.html')

def createMovieForm(request):
        form = MovieForm()
        if request.method == 'POST':
             form = MovieForm(request.POST)
             if form.is_valid():
                  form.save()
                  return redirect('movies_list')             
        return render(request, 'movie_create_form.html', {'form': form})


def updateMovieReview(request, pk):
    movieReview = Movie.objects.get(id=pk)
    form = MovieForm(instance=movieReview)
    if request.method == 'POST':
        form = MovieForm(request.POST, instance=movieReview)
        if form.is_valid():
             form.save()
             return redirect('movies_list')
    return render(request, 'movie_create_form.html', {'form': form})

def deleteMovieReview(request, pk):
     movieReview = Movie.objects.get(id=pk)
     if request.method == 'POST':
          movieReview.delete()
          return redirect('movies_list')
     return render(request, 'delete.html', {'obj':movieReview})
    
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