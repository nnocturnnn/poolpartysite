from django.db import models

# Create your models here.



class Urls(models.Model):
    link = models.CharField(max_length=500)
    active = models.BooleanField()

    def __str__(self):
        return self.link