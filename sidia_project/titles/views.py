from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets
from .serializers import TitleSerializer, TitleRatingSerializer, ActorSerializer, RatingSerializer, TitleActorSerializer
from .models import Title, Actor, Rating, TitleActor

# Create your views here.

class TitleView(viewsets.ModelViewSet): 
    #serializer_class = TitleSerializer
    
    def get_title_by_type(self, title_type):
        self.queryset = Title.objects.get(title_type__exact=title_type).filter(is_adult__exact=False)    #ignore
        output_json = TitleSerializer.serialize('json', self.queryset)
        return HttpResponse(output_json)

    def get_title_by_genre(self, genre):
        self.queryset = Title.extra(where=['%s in genre'], params=[genre]).filter(is_adult__exact=False)
        output_json = TitleSerializer.serialize('json', self.queryset)
        return HttpResponse(output_json)
    
    def get_all_title(self):
        self.queryset = Title.objects.all().filter(is_adult__exact=False)    #ignore
        output_json = TitleSerializer.serialize('json', self.queryset)
        return HttpResponse(output_json)

    def get_top_titles(self, year=None):
        if (year):
            self.queryset = Title.objects.select_related('tbl_rating').filter(start_year__exact=year, is_adult__exact=False).order_by('-average_rating')[:10]
        else:
            self.queryset = Title.objects.select_related('tbl_rating').filter(is_adult__exact=False).order_by('-average_rating')
        output_json = TitleRatingSerializer.serialize('json', self.queryset)
        return HttpResponse(output_json)

    # def index(request):
    #     latest_question_list = Question.objects.order_by('-pub_date')[:5]
    #     output = ', '.join([q.question_text for q in latest_question_list])
    #     return HttpResponse(output)


class ActorView(viewsets.ModelViewSet): 
    #serializer_class = ActorSerializer
    
    def get_all_actors(self):
        self.queryset = Actor.objects.all()


class RatingView(viewsets.ModelViewSet): 
    #serializer_class = RatingSerializer

    def get_all_ratings(self):
        self.queryset = Rating.objects.all()

class TitleActorView(viewsets.ModelViewSet): 
    #serializer_class = TitleActorSerializer

    def get_all_title_actors(self):
        self.queryset = TitleActor.objects.all()

def index(request):
    return HttpResponse("Hello, world. You're at the app index.")

