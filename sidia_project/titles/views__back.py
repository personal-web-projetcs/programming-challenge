from django.shortcuts import render
from django.core import serializers as s
from django.shortcuts import get_object_or_404
from django.db.models import Count, Value, F

from django.db.models.functions import Now

from rest_framework.settings import api_settings
from rest_framework.renderers import JSONRenderer
from rest_framework.views import APIView
from rest_framework.pagination import CursorPagination, PageNumberPagination, LimitOffsetPagination
from rest_framework import mixins
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework import filters

from .serializers import TitleSerializer, TitleRatingSerializer, ActorSerializer, RatingSerializer, TitleActorSerializer, TypesSerializer, ManyTypesSerializer, DashboardSerializer, TitleDashSerializer
from .models import Title, Actor, Rating, TitleActor
import json

# Create your views here.

class CustomPagination(PageNumberPagination):
    page_size = 10
    def get_paginated_response(self, data):
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'count': self.page.paginator.count,
            'results': data
        })

class CursorSetPagination(CursorPagination):
    page_size = 10
    #max_page_size = 10
    

class TitleList(generics.ListCreateAPIView):
    pagination_class = CursorSetPagination
    pagination_class.ordering = 'title_id'

    queryset = Title.objects.select_related('rating').exclude(is_adult__exact=True).exclude(rating__average_rating__lt=6)
    serializer_class = TitleRatingSerializer


class TypesList(generics.ListCreateAPIView):
    queryset = Title.objects.raw('SELECT DISTINCT ON (title_type) title_type, title_id FROM tbl_title ORDER BY title_type, title_id')
    serializer_class = TypesSerializer


class TitleTypeList(generics.ListCreateAPIView):
    pagination_class = CursorPagination
    pagination_class.ordering = 'title_id'
    pagination_class.page_size = 10
    #pagination_class.max_page_size = 50

    serializer_class = TitleSerializer

    def get_queryset(self):
        t = self.kwargs['title_type']
        return Title.objects.filter(title_type=t)

class ManyTypesList(viewsets.ModelViewSet):
    pagination_class = CursorSetPagination
    serializer_class = TitleSerializer
     
    def get_queryset(self):
        p = self.request.data
        return Title.objects.filter(title_type__in=p.values()).order_by('title_id').select_related('rating').exclude(is_adult__exact=True).exclude(rating__average_rating__lt=6)
        

class TitleGenreList(generics.ListCreateAPIView):
    pagination_class = CursorPagination
    pagination_class.ordering = 'title_id'
    pagination_class.page_size = 10
    # pagination_class.max_page_size = 50

    serializer_class = TitleSerializer

    def get_queryset(self):
        t = self.kwargs['genre']
        return Title.objects.filter(genres__contains=[t])


class TopList(generics.ListCreateAPIView): 
    pagination_class = PageNumberPagination
    pagination_class.page_size = 10
    
    serializer_class = TitleRatingSerializer

    def get_queryset(self):
        try:
            y = self.kwargs['year']
            queryset = self.get_data_by_year(y)
            return queryset
        except:
            queryset = self.get_full_top_list()
            return queryset
    
    def get_data_by_year(self, year):
        return Title.objects.filter(start_year__exact=year).select_related('rating').exclude(is_adult__exact=True).exclude(rating__average_rating__lt=6).exclude(rating__average_rating__exact=None).order_by('-rating__average_rating', 'title_id')

    def get_full_top_list(self):
        return Title.objects.select_related('rating').exclude(is_adult__exact=True).exclude(rating__average_rating__lt=6).exclude(rating__average_rating__exact=None).order_by('-rating__average_rating', 'title_id')

# class TopList(generics.ListCreateAPIView):
#     pagination_class = CursorSetPagination
#     pagination_class.page_size = 10
#     pagination_class.ordering = 'ts'
#     serializer_class = TitleRatingSerializer

#     def get_queryset(self):
#         try:
#             y = self.kwargs['year']
#             queryset = self.get_data_by_year(y)
#             return queryset
#         except:
#             queryset = self.get_full_top_list()
#             return queryset
    
#     def get_data_by_year(self, year):
#         return Title.objects.filter(start_year__exact=year).select_related('rating').exclude(is_adult__exact=True).exclude(rating__average_rating__lt=6).exclude(rating__average_rating__exact=None).order_by('-rating__average_rating')

#     def get_full_top_list(self):
        
#         return Title.objects.select_related('rating').exclude(is_adult__exact=True).exclude(rating__average_rating__lt=6).exclude(rating__average_rating__exact=None).order_by('title_id').order_by('-rating__average_rating').annotate(ts=Now()-start_date)


class TitleCountView(APIView):
    renderer_classes = (JSONRenderer, )

    def get(self, request, format=None):
        title_count = Title.objects.count()
        content = {'title_count': title_count}
        return Response(content)

class ActorCountView(APIView):
    renderer_classes = (JSONRenderer, )

    def get(self, request, format=None):
        actor_count = Actor.objects.count()
        content = {'actor_count': actor_count}
        return Response(content)

class TypeCountView(APIView):
    renderer_classes = (JSONRenderer, )

    def get(self, request, format=None):
        type_count = Title.objects.values('title_type').annotate(qty=Count('title_type'))
        content = {'type_count': type_count}
        return Response(content)

class CompletedDataView(APIView):
    renderer_classes = (JSONRenderer, )

    def get(self, request, format=None):
        completed_count = Title.objects.select_related('tbl_rating').exclude(start_year__exact=None).exclude(end_year__exact=None).exclude(runtime_minutes__exact=None) \
                                                                    .exclude(genres__exact=None).exclude(rating__average_rating__exact=None).exclude(rating__num_votes__exact=None).count()
        content = {'completed': completed_count}
        return Response(content)

class AdultCountView(APIView):
    renderer_classes = (JSONRenderer, )

    def get(self, request, format=None):
        adult_count = Title.objects.filter(is_adult__exact=True).count()
        content = {'adult': adult_count}
        return Response(content)

class WorstRatingView(APIView):
    renderer_classes = (JSONRenderer, )

    def get(self, request, format=None):
        worst_count = Title.objects.select_related('rating').filter(rating__average_rating__lt=6).count()
        content = {'worst': worst_count}
        return Response(content)
    




