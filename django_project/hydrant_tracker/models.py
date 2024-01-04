from django.db import models

class MapPoint(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
    status = models.CharField(max_length=100)
    pressure = models.FloatField()

    def __str__(self):
        return f"Point({self.latitude}, {self.longitude})"
