from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import Movie
from .forms import MovieReviewForm
# Create your views here.



def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def reviews(request):
    movies = Movie.objects.all()
    return render(request, 'reviews.html', {'movies': movies})

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
        password = request.POST.get('password')
        password_again = request.POST.get('password-again')

        if password != password_again:
            error = "Passwords do not match"
            return render(request, 'register_page.html', {'error': error})
        
        if User.objects.filter(username=username).exists():
            error = "Username is already taken"
            return render(request, 'register_page.html', {'error': error})
        
        user = User.objects.create_user(username=username, password=password)
        return redirect('login')
     return render(request, 'register_page.html', {'error': error})

def movie(request, pk):
     return render(request, 'movie.html')

def createMovieReview(request):
        form = MovieReviewForm()
        if request.method == 'POST':
             form = MovieReviewForm(request.POST)
             if form.is_valid():
                  form.save()
                  return redirect('reviews')
                
        return render(request, 'reviews_form.html', {'form': form})

def updateMovieReview(request, pk):
    movieReview = Movie.objects.get(id=pk)
    form = MovieReviewForm(instance=movieReview)

    if request.method == 'POST':
        form = MovieReviewForm(request.POST, instance=movieReview)
        if form.is_valid():
             form.save()
             return redirect('reviews')

    return render(request, 'reviews_form.html', {'form': form})

def deleteMovieReview(request, pk):
     movieReview = Movie.objects.get(id=pk)

     if request.method == 'POST':
          movieReview.delete()
          return redirect('reviews')
     return render(request, 'delete.html', {'obj':movieReview})
    
    
