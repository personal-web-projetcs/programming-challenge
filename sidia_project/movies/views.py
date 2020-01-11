from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets
from .serializers import MovieSerializer, ActorSerializer, RatingSerializer, MovieActorSerializer
from .models import Movie, Actor, Rating, MovieActor

# Create your views here.

class MovieView(viewsets.ModelViewSet): 
    serializer_class = MovieSerializer
    queryset = Movie.objects.all()    #ignore

class ActorView(viewsets.ModelViewSet): 
    serializer_class = ActorSerializer
    queryset = Actor.objects.all()

class RatingView(viewsets.ModelViewSet): 
    serializer_class = RatingSerializer
    queryset = Rating.objects.all()

class MovieActorView(viewsets.ModelViewSet): 
    serializer_class = MovieActorSerializer
    queryset = MovieActor.objects.all()

def index(request):
    return HttpResponse("Hello, world. You're at the app index.")

