from django.db import models

# Create your models here.

class student(models.Model):
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    