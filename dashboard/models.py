from datetime import datetime
from django.db import models


# Create your models here.

class Cycletime(models.Model):
    partno = models.CharField(max_length=50)
    create_at_date = models.DateField(auto_now=True,null=True)
    create_at_time = models.TimeField(null=True)

class PartNO(models.Model):
    partnumber = models.CharField(max_length=20)
    cycletime = models.FloatField()

