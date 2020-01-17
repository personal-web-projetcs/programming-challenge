from django.shortcuts import render
from django.http import HttpResponse
from django.http import Http404
from django.core import serializers as s
from django.shortcuts import get_object_or_404
import psycopg2

from rest_framework.pagination import CursorPagination, PageNumberPagination
from rest_framework import mixins
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status

from .serializers import TitleSerializer, TitleRatingSerializer, ActorSerializer, RatingSerializer, TitleActorSerializer, TypesSerializer, ManyTypesSerializer
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
    
    # def list(self, request):
        
    #     p = request.data
    #     queryset = Title.objects.filter(title_type__in=p.values())[:10]
    #     serializer = TitleSerializer(queryset, many=True)
    #     return Response(serializer.data)

    # def get_serializer_class(self):
    #     if self.action == 'list':
    #         serializer = TitleSerializer
    #     elif self.action == 'retrieve':
    #         serializer = ManyTypesSerializer
    #     return serializer
        

class TitleGenreList(generics.ListCreateAPIView):
    pagination_class = CursorPagination
    pagination_class.ordering = 'title_id'
    pagination_class.page_size = 10
    # pagination_class.max_page_size = 50

    serializer_class = TitleSerializer

    def get_queryset(self):
        t = self.kwargs['genre']
        return Title.objects.filter(genres__contains=[t])

# class TitleTopList(generics.ListCreateAPIView):
    
#     # pagination_class.ordering = '-average_rating'
#     serializer_class = TitleRatingSerializer

#     def get_queryset(self):
#         try:
#             y = self.kwargs['year']
#             pagination_class = None
#             return Title.objects.filter(start_year__exact=y).select_related('rating').exclude(is_adult__exact=True).exclude(rating__average_rating__lt=6).exclude(rating__average_rating__exact=None).order_by('-rating__average_rating')[:10]
#         except:
#             self.pagination_class = CursorPagination
#             # self.pagination_class.max_page_size = 50
#             self.pagination_class.page_size = 10
#             self.pagination_class.ordering = '-average_rating'

#             return Title.objects.all().select_related('rating').exclude(is_adult__exact=True).exclude(rating__average_rating__lt=6).exclude(rating__average_rating__exact=None)

# class TopListByYear(generics.ListCreateAPIView):
#     pagination_class = CustomPagination
#     serializer_class = TitleRatingSerializer

#     def get_queryset(self):
#         y = self.kwargs['year']
#         return Title.objects.filter(start_year__exact=y).select_related('rating').exclude(is_adult__exact=True).exclude(rating__average_rating__lt=6).exclude(rating__average_rating__exact=None).order_by('-rating__average_rating')[:10]

# class TopList(viewsets.ModelViewSet):
#     pagination_class = CustomPagination
#     serializer_class = TitleRatingSerializer
#     # queryset = Title.objects.select_related('rating').exclude(is_adult__exact=True).exclude(rating__average_rating__lt=6).exclude(rating__average_rating__exact=None).order_by('-rating__average_rating')

#     def get_queryset(self):
#         return Title.objects.select_related('rating').exclude(is_adult__exact=True).exclude(rating__average_rating__lt=6).exclude(rating__average_rating__exact=None).order_by('title_id').order_by('-rating__average_rating')

class TopList(viewsets.ModelViewSet):
    pagination_class = CustomPagination
    serializer_class = TitleRatingSerializer
    # queryset = Title.objects.select_related('rating').exclude(is_adult__exact=True).exclude(rating__average_rating__lt=6).exclude(rating__average_rating__exact=None).order_by('-rating__average_rating')

    def get_queryset(self):
        try:
            y = self.kwargs['year']
            return Title.objects.filter(start_year__exact=y).select_related('rating').exclude(is_adult__exact=True).exclude(rating__average_rating__lt=6).exclude(rating__average_rating__exact=None).order_by('-rating__average_rating')[:10]
        except:
            return Title.objects.select_related('rating').exclude(is_adult__exact=True).exclude(rating__average_rating__lt=6).exclude(rating__average_rating__exact=None).order_by('title_id').order_by('-rating__average_rating')

# class TitleDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Title.objects.all()[:20]
#     serializer_class = TitleSerializer



