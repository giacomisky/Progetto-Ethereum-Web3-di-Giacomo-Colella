from django.contrib import admin
from .models import Customer, Wallet
# Register your models here.

admin.site.register([Customer, Wallet])
