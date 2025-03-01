# Generated by Django 5.1.3 on 2025-01-11 10:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0023_delete_reviewvote'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='actors',
            field=models.ManyToManyField(blank=True, related_name='movies_directed', to='app.movieperson'),
        ),
        migrations.AlterField(
            model_name='movie',
            name='picture',
            field=models.ImageField(blank=True, null=True, upload_to='movie_pictures/'),
        ),
    ]
