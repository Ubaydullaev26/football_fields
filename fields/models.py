from django.db import models
from django.conf import settings
from django.contrib.gis.db import models as gis_models
from django_filters import rest_framework as filters
from django.utils.translation import gettext_lazy as _



class Field(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='fields', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    contact = models.CharField(max_length=50)
    images = models.ImageField(upload_to='field_images/', null=True, blank=True)
    hourly_rate = models.DecimalField(max_digits=6, decimal_places=2)
    location = gis_models.PointField(spatial_index=True)  # (longitude, latitude)

    # latitude = models.FloatField()
    # longitude = models.FloatField()
    
    class Meta:
        db_table = 'football'
        verbose_name = _('Field')
        verbose_name_plural = _('Fields')
        indexes = [
            models.Index(fields=['name'], name='field_name_idx'),
        ]


    def __str__(self):
        return self.name
    
    
class FieldFilter(filters.FilterSet):
    class Meta:
        model = Field
        fields = {
            'name': ['icontains'],
            'address': ['icontains'],
        }