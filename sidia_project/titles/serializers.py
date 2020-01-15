from rest_framework import serializers
from .models import Title, Actor, Rating, TitleActor

class TitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Title
        #fields = ('title_id', 'tconst', 'title_type', 'primary_title', 'original_title', 'is_adult', 'start_year', 'end_year', 'runtime_minutes', 'genres')
        fields = ('title_id', 'title_type', 'original_title', 'is_adult', 'start_year', 'end_year', 'runtime_minutes', 'genres')

class TypesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Title
        fields = ('title_type', 'title_id')

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ('average_rating', 'num_votes')

class TitleRatingSerializer(serializers.ModelSerializer):
    rating = RatingSerializer(read_only=True)
    class Meta:
        model = Title
        fields = ('title_id', 'title_type', 'original_title', 'is_adult', 'start_year', 'end_year', 'runtime_minutes', 'genres', 'rating')

class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = ('actor_id', 'nconst', 'primary_name', 'birth_year', 'death_year', 'primary_profession')

class TitleActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = TitleActor
        fields = ('title_id', 'actor_id')