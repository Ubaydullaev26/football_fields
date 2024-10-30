# from django.contrib import admin
# from .models import Field


# @admin.register(Field)
# class FieldAdmin(admin.ModelAdmin):
#     list_display = ('name', 'owner', 'hourly_rate')
#     search_fields = ('name', 'owner__username')


from django.contrib import admin
from django.contrib.gis import admin as gis_admin
from .models import Field  # Replace with the name of your model

class FieldAdmin(gis_admin.OSMGeoAdmin):
    # Configure the OSMGeoAdmin to use the map widget
    list_display = ('name', 'owner', 'hourly_rate')
    search_fields = ('name', 'owner__username')
    map_widget = gis_admin.OpenLayersWidget

admin.site.register(Field, FieldAdmin)