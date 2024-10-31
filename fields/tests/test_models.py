from django.test import TestCase
from fields.models import FootballField
from django.contrib.auth import get_user_model

User = get_user_model()

class FootballFieldModelTest(TestCase):
    
    def setUp(self):
        self.owner = User.objects.create_user(username='testowner', password='password123')
        self.field = FootballField.objects.create(
            owner=self.owner,
            name="Test Field",
            address="123 Test Address",
            contact="1234567890",
            hourly_rate=100.0,
            latitude=40.7128,
            longitude=-74.0060,
            is_active=True
        )

    def test_field_creation(self):
        self.assertEqual(self.field.name, "Test Field")
        self.assertEqual(self.field.address, "123 Test Address")
        self.assertEqual(self.field.contact, "1234567890")
        self.assertEqual(self.field.hourly_rate, 100.0)
        self.assertTrue(self.field.is_active)

    def test_field_owner(self):
        self.assertEqual(self.field.owner, self.owner)
