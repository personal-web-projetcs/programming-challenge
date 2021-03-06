"""djangoconfig URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from titles import views
from rest_framework.urlpatterns import format_suffix_patterns


urlpatterns = [

    path('api/titles/', views.TitleList.as_view()),

    path('api/titles/types/', views.TypesList.as_view()),

    path('api/titles/types/filter/', views.ManyTypesList.as_view({'post': 'list'})),

    path('api/titles/type/<str:title_type>/', views.TitleTypeList.as_view()),
    path('api/titles/genre/<str:genre>/', views.TitleGenreList.as_view()),

    path('api/titles/genres/', views.GenreList.as_view({'get': 'list'})),

    # path('api/titles/top/', views.TopListFiltered.as_view({'post': 'list'})),
    # path('api/titles/top/<str:year>/', views.TopListFiltered.as_view({'post': 'list'})),

    path('api/titles/top/', views.TopList.as_view({'get': 'list', 'post': 'list'})),
    path('api/titles/top/<str:year>/', views.TopList.as_view({'get': 'list', 'post': 'list'})),
    
    
    path('api/titles/stat/title/', views.TitleCountView.as_view()),
    path('api/titles/stat/actor/', views.ActorCountView.as_view()),
    path('api/titles/stat/type/', views.TypeCountView.as_view()),
    path('api/titles/stat/completed/', views.CompletedDataView.as_view()),
    path('api/titles/stat/adult/', views.AdultCountView.as_view()),
    path('api/titles/stat/worst/', views.WorstRatingView.as_view()),

    #path('index/', include('titles.urls')),
    path('admin/', admin.site.urls),
]

urlpatterns = format_suffix_patterns(urlpatterns)
