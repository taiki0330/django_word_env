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

    def __str__(self):
        return self.title