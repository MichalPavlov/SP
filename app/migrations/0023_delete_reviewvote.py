# Generated by Django 5.1.3 on 2025-01-11 09:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0022_alter_review_rating'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ReviewVote',
        ),
    ]
