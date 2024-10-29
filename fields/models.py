from django.db import models
from django.conf import settings

class Field(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='fields', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    contact = models.CharField(max_length=50)
    images = models.ImageField(upload_to='field_images/', null=True, blank=True)
    hourly_rate = models.DecimalField(max_digits=6, decimal_places=2)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return self.name