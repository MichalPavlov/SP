from django.shortcuts import render, redirect
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
    return render(request, 'login_page.html')

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
    
    
