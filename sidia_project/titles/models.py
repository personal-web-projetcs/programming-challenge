from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.

class Title(models.Model):
    titleId = models.AutoField(primary_key=True)
    tconst = models.CharField(max_length=20)
    titleType = models.CharField(max_length=20)
    primaryTitle = models.CharField(max_length=100)
    originalTitle = models.CharField(max_length=100)
    isAdult = models.BooleanField()
    startYear = models.IntegerField(validators=[MinValueValidator(1, message='The year must be at least 1'), 
                                                MaxValueValidator(9999, message='The year must be up to 9999')], 
                                    null=True)
    endYear = models.IntegerField(validators=[MinValueValidator(1, message='The year must be at least 1'), 
                                                MaxValueValidator(9999, message='The year must be up to 9999')], 
                                  null=True)
    runtimeMinutes = models.IntegerField(validators=[MinValueValidator(1, message='The runtime of title must be at least 1')], null=True)
    genres = ArrayField(models.CharField(max_length=20), size=3, null=True)
    
    def __str__(self):
        return self.originalTitle + '\nDuration - ' + str(self.runtimeMinutes) + '\n' + str(self.startYear)
    
    class Meta:
        db_table = 'tbl_title'

class Rating(models.Model):
    titleId = models.OneToOneField('Title', on_delete=models.CASCADE, to_field='titleId', primary_key=True)
    averageRating = models.FloatField()
    numVotes = models.IntegerField(validators=[MinValueValidator(0, message='The number of votes must be at least 0')])

    def __str__(self):
        return str(self.numVotes) + ' votes'
    
    class Meta:
        db_table = 'tbl_rating'

class Actor(models.Model):
    actorId = models.AutoField(primary_key=True)
    nconst = models.CharField(max_length=20)
    primaryName = models.CharField(max_length=30)
    birthYear = models.IntegerField(validators=[MinValueValidator(1, message='The year must be at least 1'), 
                                                MaxValueValidator(9999, message='The year must be up to 9999')], 
                                  null=True)
    deathYear = models.IntegerField(validators=[MinValueValidator(1, message='The year must be at least 1'), 
                                                MaxValueValidator(9999, message='The year must be up to 9999')], 
                                  null=True)
    primaryProfession = ArrayField(models.CharField(max_length=20), size=3, null=True)

    def __str__(self):
        return self.primaryName
    
    class Meta:
        db_table = 'tbl_actor'

class TitleActor(models.Model):
    titleId = models.ForeignKey('Title', on_delete=models.CASCADE, to_field='titleId')
    actorId = models.ForeignKey('Actor', on_delete=models.CASCADE, to_field='actorId')

    class Meta:
        db_table = 'tbl_title_actor'

class DataImportApp(object):
    def importFile(self, separator):
        pass
    
