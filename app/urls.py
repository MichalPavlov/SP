from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('about/', views.about, name="about"),
    path('reviews/', views.reviews, name="reviews"),
    path('create-movieReview/', views.createMovieReview, name="create-movieReview"),
    path('update-movieReview/<str:pk>/', views.updateMovieReview, name="update-movieReview")
]

