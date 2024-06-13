from django.db import models

class User(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    pw = models.CharField(max_length=1000)

