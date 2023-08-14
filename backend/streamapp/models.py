from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.core.validators import RegexValidator

class Movie(models.Model):
    id = models.CharField(primary_key=True, max_length=15, error_messages={'unique': 'This ID is already in use !'})
    title = models.CharField(max_length=100)
    cast = ArrayField(models.CharField(max_length=50))
    genres = ArrayField(models.CharField(max_length=20))
    runtime = models.IntegerField()
    country = ArrayField(models.CharField(max_length=5))
    language = ArrayField(models.CharField(max_length=5))
    year = models.IntegerField()
    director = ArrayField(models.CharField(max_length=50))
    rating = models.FloatField()
    votes = models.IntegerField()
    production = ArrayField(models.CharField(max_length=50))
    cover = models.CharField(max_length=250)
    plot = models.CharField(max_length=10000)

class User(models.Model):
    fname = models.CharField(max_length=16, validators=[RegexValidator(regex=r'^[a-zA-z]+$', message='Name should only contain letters')])
    lname = models.CharField(max_length=16, validators=[RegexValidator(regex=r'^[a-zA-z]+$', message='Name should only contain letters')])
    email = models.EmailField(unique=True, error_messages={'unique': 'This Email is already in use !'})
    username = models.CharField(primary_key=True, max_length=16, error_messages={'unique': 'This Username is already in use !'}, validators=[RegexValidator(regex=r'^[a-zA-z0-9_]+$', message='Username can contain only letters, numbers and underscores')])
    password = models.CharField(max_length=250)
    DOB = models.CharField(max_length=15)
    likes = models.JSONField(blank=True, null=True)
    watched = models.JSONField(blank=True, null=True)
    watch_list = models.JSONField(blank=True, null=True)

