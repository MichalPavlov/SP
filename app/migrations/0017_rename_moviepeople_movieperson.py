# Generated by Django 5.1.3 on 2025-01-08 16:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0016_rename_title_movie_name'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='MoviePeople',
            new_name='MoviePerson',
        ),
    ]
