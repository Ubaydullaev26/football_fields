from django.contrib import admin
from .models import Field

@admin.register(Field)
class FieldAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'hourly_rate')
    search_fields = ('name', 'owner__username')