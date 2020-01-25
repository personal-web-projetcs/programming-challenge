from django.shortcuts import render
from django.core import serializers as s
from django.shortcuts import get_object_or_404
from django.db.models import Count, Value, Q
import logging

from rest_framework.renderers import JSONRenderer
from rest_framework.views import APIView
from rest_framework.pagination import CursorPagination, PageNumberPagination
from rest_framework import mixins
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status

from .serializers import TitleSerializer, TitleRatingSerializer, ActorSerializer, RatingSerializer, TitleActorSerializer, TypesSerializer, GenresSerializer, ManyTypesSerializer, DashboardSerializer, TitleDashSerializer
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

class GenreList(viewsets.ModelViewSet):
    sql_code = '''SELECT DISTINCT ON (s.genres) s.genres as genre, s.title_id FROM ( SELECT DISTINCT ON (genres[1]) genres[1], title_id FROM tbl_title
                        UNION SELECT DISTINCT ON (genres[2]) genres[2], title_id FROM tbl_title
                        UNION SELECT DISTINCT ON (genres[3]) genres[3], title_id FROM tbl_title ) AS s  WHERE s.genres IS NOT NULL'''
    queryset = Title.objects.raw(sql_code)
    serializer_class = GenresSerializer
        

class TitleGenreList(generics.ListCreateAPIView):
    pagination_class = CursorPagination
    pagination_class.ordering = 'title_id'
    pagination_class.page_size = 10
    # pagination_class.max_page_size = 50

    serializer_class = TitleSerializer

    def get_queryset(self):
        t = self.kwargs['genre']
        return Title.objects.filter(genres__contains=[t])


# class TopListFiltered(viewsets.ModelViewSet):
#     pagination_class = CustomPagination
#     serializer_class = TitleRatingSerializer

#     def get_queryset(self):
#         logger = logging.getLogger(__name__)
#         logger.error("Get Queryset")
#         try:
#             y = self.kwargs['year']
#             return self.perform_query(y)
#         except Exception as e:
#             print(e)
#             return self.perform_query()

#     def perform_query(self, year=None):
#         dataset = []
#         logger = logging.getLogger(__name__)
#         if (year):
#             logger.error('With YEar >>>>>')
#             g = self.request.data["genres"]["data"]
#             print(g)
#             q = Q()
#             for value in g:
#                 q |= Q(genres__contains=[value])
#             dataset = Title.objects.filter(start_year__exact=year).filter(q).select_related('rating').exclude(is_adult__exact=True).exclude(rating__average_rating__lt=6).exclude(rating__average_rating__exact=None).order_by('-rating__average_rating', 'title_id')

#         else:
#             logger.error('Without YEar >>>>>')
#             g = self.request.data['genres']['data']

#             q = Q()
#             for value in g:
#                 q |= Q(genres__contains=[value])

#             dataset = Title.objects.filter(q).select_related('rating').exclude(is_adult__exact=True).exclude(rating__average_rating__lt=6).exclude(rating__average_rating__exact=None).order_by('-rating__average_rating', 'title_id')
            
#         return dataset

class TopList(viewsets.ModelViewSet):
    pagination_class = CustomPagination
    serializer_class = TitleRatingSerializer

    def get_queryset(self):
        logger = logging.getLogger(__name__)
        logger.error("Get Queryset")
        logger.error(str(self.request.POST))
        logger.error(str(self.request.GET))
        try:
            y = self.kwargs['year']
            return self.perform_query(y)
        except:
            return self.perform_query()

    def perform_query(self, year=None):
        dataset = []
        logger = logging.getLogger(__name__)

        if (year):
            logger.error('With YEar >>>>>')

            if (self.request.method == 'POST'):
                g = self.request.data["genres"]["data"]
                print(g)
                q = Q()
                for value in g:
                    q |= Q(genres__contains=[value])
                dataset = Title.objects.filter(start_year__exact=year).filter(q).select_related('rating').exclude(is_adult__exact=True).exclude(rating__average_rating__lt=6).exclude(rating__average_rating__exact=None).order_by('-rating__average_rating', 'title_id')    
            elif (self.request.method == 'GET'):
                dataset = Title.objects.filter(start_year__exact=year).select_related('rating').exclude(is_adult__exact=True).exclude(rating__average_rating__lt=6).exclude(rating__average_rating__exact=None).order_by('-rating__average_rating', 'title_id')            
        
        else:
            logger.error('Without YEar >>>>>')
            
            if (self.request.method == 'POST'):
                g = self.request.data["genres"]["data"]
                print(g)
                q = Q()
                for value in g:
                    q |= Q(genres__contains=[value])
                dataset = Title.objects.filter(q).select_related('rating').exclude(is_adult__exact=True).exclude(rating__average_rating__lt=6).exclude(rating__average_rating__exact=None).order_by('-rating__average_rating', 'title_id')    
            elif (self.request.method == 'GET'):
                dataset = Title.objects.select_related('rating').exclude(is_adult__exact=True).exclude(rating__average_rating__lt=6).exclude(rating__average_rating__exact=None).order_by('-rating__average_rating', 'title_id')


        return dataset

# class TopList(viewsets.ModelViewSet):
#     pagination_class = CustomPagination
#     serializer_class = TitleRatingSerializer

#     def get_queryset(self):
#         logger = logging.getLogger(__name__)
#         logger.error("Get Queryset")
#         logger.error(str(self.request.POST))
#         logger.error(str(self.request.GET))
#         try:
#             y = self.kwargs['year']
#             return self.perform_query(y)
#         except:
#             return self.perform_query()

#     def perform_query(self, year=None):
#         dataset = []
#         logger = logging.getLogger(__name__)
#         if (year):
#             logger.error('With YEar >>>>>')
#             dataset = Title.objects.filter(start_year__exact=year).select_related('rating').exclude(is_adult__exact=True).exclude(rating__average_rating__lt=6).exclude(rating__average_rating__exact=None).order_by('-rating__average_rating', 'title_id')
#         else:
#             logger.error('Without YEar >>>>>')
#             dataset = Title.objects.select_related('rating').exclude(is_adult__exact=True).exclude(rating__average_rating__lt=6).exclude(rating__average_rating__exact=None).order_by('-rating__average_rating', 'title_id')
#         return dataset

# class TopList(viewsets.ModelViewSet):
#     pagination_class = CustomPagination
#     serializer_class = TitleRatingSerializer

#     def get_queryset(self):
#         try:
#             y = self.kwargs['year']
#             return Title.objects.filter(start_year__exact=y).select_related('rating').exclude(is_adult__exact=True).exclude(rating__average_rating__lt=6).exclude(rating__average_rating__exact=None).order_by('-rating__average_rating', 'title_id')
#         except:
#             return Title.objects.select_related('rating').exclude(is_adult__exact=True).exclude(rating__average_rating__lt=6).exclude(rating__average_rating__exact=None).order_by('-rating__average_rating', 'title_id')


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
    




