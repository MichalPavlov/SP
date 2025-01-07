from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('about/', views.about, name="about"),
    path('movies_list/', views.movies_list, name="movies_list"),
    path('create-movieReview/', views.createMovieReview, name="create-movieReview"),
    path('update-movieReview/<str:pk>/', views.updateMovieReview, name="update-movieReview"),
    path('delete-movieReview/<str:pk>/', views.deleteMovieReview, name="delete-movieReview"),
    path('movie/<str:pk>/', views.movie, name="movie"),
    path('login/', views.login_page, name="login"),
    path('logout/', views.logout_user, name="logout"),
    path('register/', views.register, name="register"),
]

