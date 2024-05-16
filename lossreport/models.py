from django.db import models
from datetime import datetime,date,time
from django.core.validators import MaxValueValidator

# Create your models here.
class Loss(models.Model):

    TYPE = (
        ('part_supply','Part Supply'),
        ('defect','Defect'),
        ('breakdown','Breakdown'),
        ('short_stop','Short Stop'),
        ('changing','Changing/Model Change'),
    )

    ABC = (
        ('A','A'),
        ('B','B'),
        ('C','C'),
    )

    TIME = (
        (time(7,40),"07:35-08:30"),
        (time(8,40),"08:30-09:30"),
        (time(9,50),"09:40-10:30"),
        (time(11,00),"10:30-11:15"),
        (time(12,30),"12:15-13:30"),
        (time(13,31),"13:30-14:30"),
        (time(14,50),"14:40-15:30"),
        (time(15,40),"15:30-16:30"),
        (time(17,00),"16:50-17:50"),
        (time(18,30),"17:50-18:40"),
        (time(18,51),"18:50-19:20"),
        (time(19,50),"19:35-20:30"),
        (time(20,40),"20:30-21:30"),
        (time(21,50),"21:40-22:30"),
        (time(22,40),"22:30-23:30"),
        (time(00,30),"00:20-01:30"),
        (time(1,40),"01:30-02:30"),
        (time(3,20),"02:50-03:30"),
        (time(3,40),"03:30-04:30"),
        (time(5,00),"04:50-05:50"),
        (time(6,00),"05:50-06:40"),
        (time(7,00),"06:40-07:20"),
    )

    problem = models.CharField(max_length=100)
    lossType = models.CharField(max_length=40, choices=TYPE)
    ABCType = models.CharField(max_length=1,default='C',choices=ABC)
    duration = models.IntegerField(validators=[MaxValueValidator(1440)])
    create_at_date = models.DateField(null=True,verbose_name='Date')
    create_at_time = models.TimeField(null=True,choices=TIME,verbose_name="Shift")

    def __str__(self):
        return self.problem

    
    

    


