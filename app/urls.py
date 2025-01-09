from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('about/', views.about, name="about"),
    path('movies_list/', views.movies_list, name="movies_list"),
    path('actors_list/', views.actors_list, name="actors_list"),
    path('directors_list/', views.directors_list, name="directors_list"),
    path('movie-create-form/', views.createMovie, name="movie-create-form"),
    path('update-movie-form/<str:pk>/', views.updateMovie, name="update-movie-form"),
    path('delete-movie-form/<str:pk>/', views.deleteMovie, name="delete-movie-form"),
    path('movie_person-create-form/', views.createMoviePersonForm, name="movie_person-create-form"),
    path('update-movie_person-form/<str:pk>/', views.updateMoviePerson, name="update-movie_person-form"),
    path('delete-movie_person-form/<str:pk>/', views.deleteMoviePerson, name="delete-movie_person-form"),
    path('review-create-form/', views.createReview, name="review-create-form"),
    path('update-review-form/<str:pk>/', views.updateReview, name="update-review-form"),
    path('delete-review-form/<str:pk>/', views.deleteReview, name="delete-review-form"),
    path('movie/<str:pk>/', views.movie, name="movie"),
    path('movie_person/<str:pk>/', views.movie_person, name="movie_person"),
    path('login/', views.login_page, name="login"),
    path('logout/', views.logout_user, name="logout"),
    path('register/', views.register, name="register"),
]

