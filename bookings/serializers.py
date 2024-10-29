from rest_framework import serializers
from .models import Booking
from django.db.models import Q

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'
        read_only_fields = ('user',)

    def validate(self, data):
        field = data['field']
        start_time = data['start_time']
        end_time = data['end_time']

        # Check for overlapping bookings
        overlapping_bookings = Booking.objects.filter(
            field=field,
            start_time__lt=end_time,
            end_time__gt=start_time
        ).exists()

        if overlapping_bookings:
            raise serializers.ValidationError("This time slot is already booked.")

        return data
