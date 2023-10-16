from django.db import models


class Photo(models.Model):
    title = models.CharField(max_length=100)
    albumId = models.IntegerField()
    width = models.IntegerField()
    height = models.IntegerField()
    color = models.CharField(max_length=6)
    url = models.ImageField(upload_to='photos')
