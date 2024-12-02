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
     form = MovieReviewForm(initial=movieReview)

     return render(request, 'reviews_form.html', {'form': form})