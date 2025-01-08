from django.contrib import admin
from .models import MoviePeople, Movie, Review, ReviewVote

admin.site.register(MoviePeople)
admin.site.register(Movie)
admin.site.register(Review)
admin.site.register(ReviewVote)