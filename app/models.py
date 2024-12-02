from django.db import models

# Create your models here.

class Movie(models.Model):
    name = models.CharField(max_length=500)
    description = models.TextField(null=True, blank=True)
    #actors =
    #director =
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)


    class Meta:
        ordering = ['-updated', '-created']
    def __str__(self):
        return self.name