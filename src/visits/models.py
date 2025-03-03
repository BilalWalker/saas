from django.db import models

# Create your models here.
class PageVisit(models.Model):
    # database table
    path = models.TextField(blank=True, null=True) # column
    timestamp = models.DateTimeField(auto_now_add=True) # column
