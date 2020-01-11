from rest_framework import serializers
from .models import Title, Actor, Rating, TitleActor

class TitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Title
        fields = ('tconst', 'titleType', 'primaryTitle', 'originalTitle', 'isAdult', 'startYear', 'endYear', 'runtimeMinutes', 'genres')

class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = ('nconst', 'primaryName', 'birthYear', 'deathYear', 'primaryProfession')

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ('tconst', 'averageRating', 'numVotes')

class TitleActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = TitleActor
        fields = ('tconst', 'nconst')