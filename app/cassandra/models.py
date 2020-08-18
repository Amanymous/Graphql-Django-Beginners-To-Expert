from django.db import models

# Create your models here.
class Cassandra(models.Model):
    FirstName = models.CharField(max_length=50)
    LastName = models.CharField(max_length=50)
    Age = models.PositiveIntegerField(null=True, blank=True)    
    Description = models.TextField(blank=True)
    url = models.URLField()
    createdAt = models.DateTimeField(auto_now_add=True)