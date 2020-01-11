from django.contrib import admin

from django.contrib import admin    #added from here
from .models import Title, Actor, TitleActor, Rating
# Register your models here.

class TitleAdmin(admin.ModelAdmin):
    list_display = ('tconst', 'titleType', 'primaryTitle', 'originalTitle', 'isAdult', 'startYear', 'endYear', 'runtimeMinutes', 'genres')

class ActorAdmin(admin.ModelAdmin):  
    list_display = ('nconst', 'primaryName', 'birthYear', 'deathYear', 'primaryProfession')

# Register your models here.
admin.site.register(Title, TitleAdmin)
admin.site.register(Actor, ActorAdmin)