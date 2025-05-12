from django.db import models


class Info(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

