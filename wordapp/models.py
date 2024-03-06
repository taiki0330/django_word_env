from django.db import models

# Create your models here.
class Division(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name




class Crime(models.Model):
    title = models.CharField(max_length=100)
    division = models.ForeignKey(Division, related_name="crimes", on_delete=models.CASCADE)
    detail = models.TextField()
    crime_name = models.CharField(max_length=100, null=True)
    crime_name_second = models.CharField(max_length=100, null=True)
    crime_start_date = models.DateField(null=True)
    crime_start_time = models.TimeField(null=True)
    crime_end_date = models.DateField(null=True)
    crime_end_time = models.TimeField(null=True)
    crime_place = models.CharField(max_length=100, null=True)

    suspect_honseki = models.CharField(max_length=100, null=True)
    suspect_address = models.CharField(max_length=100, null=True)
    suspect_job = models.CharField(max_length=100, null=True)
    suspect_name = models.CharField(max_length=100, null=True)
    suspect_birthday = models.CharField(max_length=100, null=True)
    
    victim_address = models.CharField(max_length=100, null=True)
    victim_job = models.CharField(max_length=100, null=True)
    victim_name = models.CharField(max_length=100, null=True)
    victim_birthday = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.title