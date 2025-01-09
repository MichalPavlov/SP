from django.db import models
from django.contrib.auth.models import User
from django.forms import ValidationError

class MoviePerson(models.Model):
    name = models.CharField(max_length=100)
    picture = models.URLField(max_length=500, null=True, blank=True)
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
    picture = models.URLField(max_length=500, null=True, blank=True)
    genre = models.CharField(max_length=100)
    description = models.TextField(max_length=500, null=True, blank=True)
    release_date = models.DateField()
    director = models.ForeignKey(MoviePerson, on_delete=models.CASCADE, null=True, blank=True, related_name='movies_played_in')
    actors = models.ManyToManyField(MoviePerson, related_name='movies_directed')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Review(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.FloatField()
    comment = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['movie', 'user'] 

    def __str__(self):
        return f'{self.movie.name} - {self.user.username}'
    
    #def like_score(self):
    #    return self.reviewvote_set.filter(vote=ReviewVote.LIKE).count() - self.reviewvote_set.filter(vote=ReviewVote.DISLIKE).count()
    
class ReviewVote(models.Model):
    LIKE = 1
    DISLIKE = -1

    VOTE_CHOICES = [
        (LIKE, 'Like'),
        (DISLIKE, 'Dislike')
    ]

    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='votes')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    vote = models.IntegerField(choices=VOTE_CHOICES)

    class Meta:
        unique_together = ['review', 'user']

    def __str__(self):
        return f'{self.review.movie.name} - {self.review.user.username} - {self.vote}'