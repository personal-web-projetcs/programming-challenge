from django.contrib import admin

from django.contrib import admin    #added from here
from .models import Movie, Actor, MovieActor, Rating
# Register your models here.

class MovieAdmin(admin.ModelAdmin):
    list_display = ('tconst', 'titleType', 'primaryTitle', 'originalTitle', 'isAdult', 'startYear', 'endYear', 'runtimeMinutes', 'genres')

class ActorAdmin(admin.ModelAdmin):  
    list_display = ('nconst', 'primaryName', 'birthYear', 'deathYear', 'primaryProfession')

# Register your models here.
admin.site.register(Movie, MovieAdmin)
admin.site.register(Actor, ActorAdmin)