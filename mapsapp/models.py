from django.db import models


class InputLocation(models.Model):
    origin_address = models.CharField(max_length=100)
    origin_name = models.CharField(max_length=100)
    destination_address = models.CharField(max_length=100)
    destination_name = models.CharField(max_length=100)


class GeoLocation(models.Model):
    origin_lat = models.DecimalField(max_digits=22, decimal_places=16, blank=True, null=True)
    origin_lon = models.DecimalField(max_digits=22, decimal_places=16, blank=True, null=True)
    destination_lat = models.DecimalField(max_digits=22, decimal_places=16, blank=True, null=True)
    destination_lon = models.DecimalField(max_digits=22, decimal_places=16, blank=True, null=True)



