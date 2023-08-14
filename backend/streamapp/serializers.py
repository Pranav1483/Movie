from rest_framework import serializers
from streamapp.models import User, Movie

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('fname',
                  'lname',
                  'email',
                  'username',
                  'password',
                  'DOB',
                  'likes',
                  'watched',
                  'watch_list',)
    
class MovieSerializer(serializers.ModelSerializer):

    class Meta:
        model = Movie
        fields = ('id',
                  'title',
                  'cast',
                  'genres',
                  'runtime',
                  'country',
                  'language',
                  'year',
                  'director',
                  'rating',
                  'votes',
                  'production',
                  'cover',
                  'plot',)