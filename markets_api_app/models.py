from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class Market(models.Model):
    # TODO: USE GIS
    market_name = models.CharField(max_length=1234)
    latitude = models.FloatField(validators=[MinValueValidator(-90.0), MaxValueValidator(90.0)])
    longitude = models.FloatField(validators=[MinValueValidator(-180.0), MaxValueValidator(180.0)])

