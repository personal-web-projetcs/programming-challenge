from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.

class Title(models.Model):
    tconst = models.CharField(max_length=20, primary_key=True)
    titleType = models.CharField(max_length=15)
    primaryTitle = models.CharField(max_length=100)
    originalTitle = models.CharField(max_length=100)
    isAdult = models.BooleanField()
    startYear = models.IntegerField(validators=[MinValueValidator(1, message='The year must be at least 1'), 
                                                MaxValueValidator(9999, message='The year must be up to 9999')])
    endYear = models.IntegerField(validators=[MinValueValidator(1, message='The year must be at least 1'), 
                                                MaxValueValidator(9999, message='The year must be up to 9999')],
                                  default=models.SET_NULL)
    runtimeMinutes = models.IntegerField(validators=[MinValueValidator(1, message='The runtime of title must be at least 1')])
    genres = models = [
        models.CharField(max_length=15),
        models.CharField(max_length=15),
        models.CharField(max_length=15)
    ]

    def __str__(self):
        return self.originalTitle + '\nDuration - ' + str(self.runtimeMinutes) + '\n' + str(self.startYear)

class Rating(models.Model):
    tconst = models.ForeignKey('Title', on_delete=models.CASCADE, to_field='tconst')
    averageRating = models.FloatField()
    numVotes = models.IntegerField(validators=[MinValueValidator(0, message='The number of votes must be at least 0')])

    def __str__(self):
        return str(self.numVotes) + ' votes'

class Actor(models.Model):
    nconst = models.CharField(max_length=20, primary_key=True)
    primaryName = models.CharField(max_length=30)
    birthYear = models.CharField(max_length=4)
    deathYear = models.CharField(max_length=4)
    primaryProfession = [
        models.CharField(max_length=20),
        models.CharField(max_length=20),
        models.CharField(max_length=20)
    ]
    def __str__(self):
        return self.primaryName

class TitleActor(models.Model):
    tconst = models.ForeignKey('Title', on_delete=models.CASCADE, to_field='tconst')
    nconst = models.ForeignKey('Actor', on_delete=models.CASCADE, to_field='nconst')

class DataImportApp(object):
    def importFile(self, separator):
        pass
    
