from django.shortcuts import render
from django.http import HttpResponse
from django.http import Http404
from django.core import serializers as s
from django.shortcuts import get_object_or_404

from rest_framework.pagination import CursorPagination
from rest_framework import mixins
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.response import Response

from .serializers import TitleSerializer, TitleRatingSerializer, ActorSerializer, RatingSerializer, TitleActorSerializer
from .models import Title, Actor, Rating, TitleActor
import json

# Create your views here.

# class CustomPagination(pagination.PageNumberPagination):
#     page_size = 100
#     page_size_query_param = 'page_size'
#     max_page_size = 200
#     def get_paginated_response(self, data):
#         return Response({
#             'links': {
#                 'next': self.get_next_link(),
#                 'previous': self.get_previous_link()
#             },
#             'count': self.page.paginator.count,
#             'results': data
#         })

class CursorSetPagination(CursorPagination):
    page_size = 20
    max_page_size = 100
    page_size_query_param = 'page_size'
    

class TitleList(generics.ListCreateAPIView):
    pagination_class = CursorPagination
    pagination_class.ordering = 'title_id'
    pagination_class.page_size = 20
    pagination_class.max_page_size = 50

    queryset = Title.objects.exclude(is_adult__exact=True)
    serializer_class = TitleSerializer


class TitleTypeList(generics.ListCreateAPIView):
    pagination_class = CursorPagination
    pagination_class.ordering = 'title_id'
    pagination_class.page_size = 20
    pagination_class.max_page_size = 50

    serializer_class = TitleSerializer

    def get_queryset(self):
        t = self.kwargs['title_type']
        return Title.objects.filter(title_type=t)

class TitleGenreList(generics.ListCreateAPIView):
    pagination_class = CursorPagination
    pagination_class.ordering = 'title_id'
    pagination_class.page_size = 20
    pagination_class.max_page_size = 50

    serializer_class = TitleSerializer

    def get_queryset(self):
        t = self.kwargs['genre']
        return Title.objects.filter(genres__contains=[t])

class TitleTopList(generics.ListCreateAPIView):
    
    # pagination_class.ordering = '-average_rating'
    serializer_class = TitleRatingSerializer

    def get_queryset(self):
        try:
            y = self.kwargs['year']
            pagination_class = None
            return Title.objects.filter(start_year__exact=y).select_related('rating').exclude(is_adult__exact=True).exclude(rating__average_rating__lt=6).exclude(rating__average_rating__exact=None).order_by('-rating__average_rating')[:10]
        except:
            self.pagination_class = CursorPagination
            self.pagination_class.max_page_size = 50
            self.pagination_class.page_size = 20
            return Title.objects.all().select_related('rating').exclude(is_adult__exact=True).exclude(rating__average_rating__lt=6).exclude(rating__average_rating__exact=None).order_by('-rating__average_rating')

    
# class TitleDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Title.objects.all()[:20]
#     serializer_class = TitleSerializer



