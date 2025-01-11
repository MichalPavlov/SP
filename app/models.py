from django.db import models
from django.contrib.auth.models import User

class MoviePerson(models.Model):
    name = models.CharField(max_length=100)
    picture = models.URLField(max_length=500)
    description = models.TextField(max_length=500, null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    director = models.BooleanField(default=False)
    actor = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    

class Movie(models.Model):
    name = models.CharField(max_length=100)
    picture = models.ImageField(upload_to='movie_pictures/')
    genre = models.CharField(max_length=100)
    description = models.TextField(max_length=500, null=True, blank=True)
    release_date = models.DateField()
    length = models.IntegerField(null=True, blank=True)
    director = models.ForeignKey(MoviePerson, on_delete=models.CASCADE, null=True, blank=True, related_name='movies_directed')
    actors = models.ManyToManyField(MoviePerson, blank=True, related_name='movies_played_in')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Review(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField(max_length=10000)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['movie', 'user'] 

    def __str__(self):
        return f'{self.movie.name} - {self.user.username}'
    
