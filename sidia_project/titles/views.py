from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets
from .serializers import TitleSerializer, ActorSerializer, RatingSerializer, TitleActorSerializer
from .models import Title, Actor, Rating, TitleActor

# Create your views here.

class TitleView(viewsets.ModelViewSet): 
    serializer_class = TitleSerializer
    queryset = Title.objects.all()    #ignore

class ActorView(viewsets.ModelViewSet): 
    serializer_class = ActorSerializer
    queryset = Actor.objects.all()

class RatingView(viewsets.ModelViewSet): 
    serializer_class = RatingSerializer
    queryset = Rating.objects.all()

class TitleActorView(viewsets.ModelViewSet): 
    serializer_class = TitleActorSerializer
    queryset = TitleActor.objects.all()

def index(request):
    return HttpResponse("Hello, world. You're at the app index.")

