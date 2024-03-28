from django.db import models

# Create your models here.
class Division(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name




class Crime(models.Model):
    division = models.ForeignKey(Division, related_name="crimes", on_delete=models.CASCADE)
    crime_name = models.CharField(max_length=100)#  このフィールドは必須
    crime_name_second = models.CharField(max_length=100, null=True, blank=True)# 任意
    crime_start_date = models.DateField(null=True, blank=True)# 日付はNULLまたは空を許容
    crime_start_time = models.TimeField(null=True, blank=True)# 時間もNULLまたは空を許容
    crime_end_date = models.DateField(null=True, blank=True)# 日付はNULLまたは空を許容
    crime_end_time = models.TimeField(null=True, blank=True)# 時間もNULLまたは空を許容
    crime_place = models.CharField(max_length=100, null=True, blank=True)# 任意
    crime_fact = models.TextField(null=True, blank=True)# 任意
    suspect_honseki = models.CharField(max_length=100, null=True, blank=True)# 任意
    suspect_address = models.CharField(max_length=100, null=True, blank=True)# 任意
    suspect_job = models.CharField(max_length=100, null=True, blank=True)# 任意
    suspect_name = models.CharField(max_length=100, null=True, blank=True)# 任意
    suspect_birthday = models.DateField(null=True, blank=True)# 日付はNULLまたは空を許容


    def __str__(self):
        return self.crime_name