from rest_framework import serializers
from .models import Movie, Actor, Rating, MovieActor

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ('tconst', 'titleType', 'primaryTitle', 'originalTitle', 'isAdult', 'startYear', 'endYear', 'runtimeMinutes', 'genres')

class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = ('nconst', 'primaryName', 'birthYear', 'deathYear', 'primaryProfession')

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ('tconst', 'averageRating', 'numVotes')

class MovieActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovieActor
        fields = ('tconst', 'nconst')