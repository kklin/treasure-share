from django.db import models

class Dribble(models.Model):
    frequency = models.IntegerField(default=0)
    percentage = models.DecimalField(max_digits=3, decimal_places=2)
    delay = models.IntegerField(default=0)

class Profile(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):              # __unicode__ on Python 2
        return self.name

class Recipients(models.Model):
    members = models.ManyToManyField(Profile, through='Membership')

class Membership(models.Model):
    profile = models.ForeignKey(Profile)
    recips = models.ForeignKey(Recipients)

class Donation(models.Model):
    donor = models.CharField(max_length=20)
    charities = models.ForeignKey(Recipients)
    amount = models.IntegerField(default=0)
    #keys =
    dribble = models.ForeignKey(Dribble)
    creation_time = models.DateTimeField()

