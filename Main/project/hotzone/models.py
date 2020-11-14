from django.db import models

class LocationDetail(models.Model):
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    xCoord = models.DecimalField(max_digits=8, decimal_places=2)
    yCoord = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return self.name