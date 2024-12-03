from django.db import models

# Create your models here.

class Movie(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    image = models.CharField(max_length=500)
    #actors =
    #director =
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)


    class Meta:
        ordering = ['-updated', '-created']
    def __str__(self):
        return self.name