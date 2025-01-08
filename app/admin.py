from django.contrib import admin
from .models import MoviePerson, Movie, Review, ReviewVote

admin.site.register(MoviePerson)
admin.site.register(Movie)
admin.site.register(Review)
admin.site.register(ReviewVote)