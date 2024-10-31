# booking/tests/test_views.py
from django.test import TestCase
from rest_framework.test import APIClient, APITestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from bookings.models import Booking
from fields.models import Field
from rest_framework import status

User = get_user_model()

class BookingAPITest(APITestCase):
    def setUp(self):
        self.field = Field.objects.create(
            name="Test Field",
            location="123 Test Location",  # Provide a value for location
            hourly_rate=100,
            owner=self.owner,
            # Add other required fields here
        )
        # Setup booking or other related objects if necessary