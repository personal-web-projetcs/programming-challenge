from django.contrib import admin

from django.contrib import admin    #added from here
from .models import Title, Actor, TitleActor, Rating
# Register your models here.

class TitleAdmin(admin.ModelAdmin):
    list_display = ('tconst', 'title_type', 'primary_title', 'original_title', 'is_adult', 'start_year', 'end_year', 'runtime_minutes', 'genres')

class ActorAdmin(admin.ModelAdmin):  
    list_display = ('nconst', 'primary_name', 'birth_year', 'death_year', 'primary_profession')

# Register your models here.
admin.site.register(Title, TitleAdmin)
admin.site.register(Actor, ActorAdmin)