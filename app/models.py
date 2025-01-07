from django.db import models
from django.contrib.auth.models import User

class Actor(models.Model):
    name = models.CharField(max_length=100)
    picture = models.URLField(max_length=500, null=True, blank=True)
    description = models.TextField(max_length=500, null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Director(models.Model):
    name = models.CharField(max_length=100)
    picture = models.URLField(max_length=500, null=True, blank=True)
    description = models.TextField(max_length=500, null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Movie(models.Model):
    title = models.CharField(max_length=100)
    picture = models.URLField(max_length=500, null=True, blank=True)
    description = models.TextField(max_length=500, null=True, blank=True)
    release_date = models.DateField()
    director = models.ForeignKey(Director, on_delete=models.CASCADE, related_name='movies')
    actors = models.ManyToManyField(Actor, related_name='movies')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

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
        return f'{self.movie.title} - {self.user.username}'
    
    def like_score(self):
        return self.votes.filter(vote=ReviewVote.LIKE).count() - self.votes.filter(vote=ReviewVote.DISLIKE).count()
    
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
        return f'{self.review.movie.title} - {self.review.user.username} - {self.value}'