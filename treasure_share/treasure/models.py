from django.db import models

class Treasure(models.Model):
    donor = models.CharField(max_length=20)
    charities =
    amount = models.IntegerField(default=0)
    keys =
    dribble =
    creation_time = models.DateTimeField()

class Dribble(models.Model):
    frequency = models.IntegerField(default=0)
    percentage = models.DecimalField(default=0)
    delay = models.IntegerField(default=0)
# Create your models here.
