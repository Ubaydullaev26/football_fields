from django.contrib import admin
from .models import Booking

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('field', 'user', 'start_time', 'end_time')
    search_fields = ('field__name', 'user__username')