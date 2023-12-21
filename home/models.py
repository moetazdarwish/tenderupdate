from django.db import models

# Create your models here.

class HomePage(models.Model):
    name = models.CharField(max_length=20,null=True,blank=True)
    text = models.TextField()