from django.db import models

class Post(models.Model):
    name = models.fields.CharField(max_length=100)
    description = models.TextField()