from django.db import models
from django.contrib.auth.models import User

#model for tokens created by the users
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    earnedToken = models.FloatField(default=0)
    prodWatt = models.FloatField(default=0)
    counter = models.FloatField(default=0)

class Wallet(models.Model):
    owner = models.ForeignKey(Customer, on_delete=models.CASCADE)
    balance = models.FloatField(blank=True, default=None)
    privateKey = models.CharField(blank=True, max_length=1600, default=None)
    address = models.CharField(blank=True, max_length=800, default=None)

