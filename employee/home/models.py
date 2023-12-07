from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime


class TimeStampModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class CustomUser(AbstractUser,TimeStampModel):
    name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    mobileno = models.CharField(max_length=15)
    role_choices = [
        ('fulltime', 'Full Time'),
        ('contract', 'Contract'),
        ('client', 'Client'),
    ]
    role = models.CharField(max_length=10, choices=role_choices)


class FullTime(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,related_name="fulltime")
    branch_name = models.CharField(max_length=100)
    
    def __str__(self):
       
        return self.branch_name

class Contract(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
    def __str__(self):
       
        return self.user


class Client(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    city_name = models.CharField(max_length=100,null=True)
    def __str__(self):
       
        return self.city_name

