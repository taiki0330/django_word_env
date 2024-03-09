from django.db import models

# Create your models here.
class Division(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name




class Crime(models.Model):
    division = models.ForeignKey(Division, related_name="crimes", on_delete=models.CASCADE)
    crime_name = models.CharField(max_length=100)
    crime_name_second = models.CharField(max_length=100, null=True, blank=True)
    crime_start_date = models.CharField(max_length=100, null=True)
    crime_start_time = models.TimeField(null=True, blank=True)
    crime_end_date = models.CharField(max_length=100, null=True)
    crime_end_time = models.TimeField(null=True, blank=True)
    crime_place = models.CharField(max_length=100, null=True)
    crime_fact = models.TextField(null=True)
    suspect_honseki = models.CharField(max_length=100, null=True, blank=True)
    suspect_address = models.CharField(max_length=100, null=True, blank=True)
    suspect_job = models.CharField(max_length=100, null=True, blank=True)
    suspect_name = models.CharField(max_length=100, null=True, blank=True)
    suspect_birthday = models.CharField(max_length=100,null=True)


    def __str__(self):
        return self.crime_name