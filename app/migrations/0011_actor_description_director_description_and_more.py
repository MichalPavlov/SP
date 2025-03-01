# Generated by Django 5.1.3 on 2025-01-07 20:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_alter_actor_picture_alter_director_picture_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='actor',
            name='description',
            field=models.TextField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='director',
            name='description',
            field=models.TextField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='movie',
            name='description',
            field=models.TextField(blank=True, max_length=500, null=True),
        ),
    ]
