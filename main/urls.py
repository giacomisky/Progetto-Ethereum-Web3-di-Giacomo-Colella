from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.homePage, name='homePage'),
    path("admin-page/", views.adminPage, name='adminPage'),
    path("login/", views.loginC, name='loginCustomer'),
    path("logout/", views.logOut, name='logOut'),
    path("check-reward/", views.checkReward, name='check-reward')
]
