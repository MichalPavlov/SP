from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import MoviePeople, Movie
from .forms import MovieReviewForm


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
    }
    return render(request, 'lists.html', {'list': list})	

def actors_list(request):
    actors = MoviePeople.objects.filter(actor=True)
    list = {
        'contents': actors,
        'type': 'actor',
        'url': 'movie_star',    
        'create_form': 'movie-create-form',
    }
    return render(request, 'lists.html', {'list': list})

def directors_list(request):
    directors = MoviePeople.objects.filter(director=True)
    list = {
        'contents': directors,
        'type': 'dirrector',
        'url': 'movie_star',
        'create_form': 'movie-create-form',
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
        form = MovieReviewForm()
        if request.method == 'POST':
             form = MovieReviewForm(request.POST)
             if form.is_valid():
                  form.save()
                  return redirect('movies_list')             
        return render(request, 'create_form.html', {'form': form})


def updateMovieReview(request, pk):
    movieReview = Movie.objects.get(id=pk)
    form = MovieReviewForm(instance=movieReview)

    if request.method == 'POST':
        form = MovieReviewForm(request.POST, instance=movieReview)
        if form.is_valid():
             form.save()
             return redirect('movies_list')
    return render(request, 'create_form.html', {'form': form})

def deleteMovieReview(request, pk):
     movieReview = Movie.objects.get(id=pk)

     if request.method == 'POST':
          movieReview.delete()
          return redirect('movies_list')
     return render(request, 'delete.html', {'obj':movieReview})
    
    
