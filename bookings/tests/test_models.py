# booking/tests/test_models.py
import datetime
from django.test import TestCase
from bookings.models import Booking
from django.contrib.auth import get_user_model

from fields.models import Field

class BookingModelTest(TestCase):
    def setUp(self):
        self.field = Field.objects.create(
            name="Sample Field",
            location="Sample Location",
            hourly_rate=100,
            owner=self.user,
            # Add other required fields here
        )
        self.booking = Booking.objects.create(
            user=self.user,
            field=self.field,
            start_time=datetime.now(),  
            end_time=datetime.now() + datetime.timedelta(hours=1),  
            status='PENDING',  # If you have a status field, set an appropriate value
        )

