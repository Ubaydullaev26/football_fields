from django.test import TestCase
from users.models import UserProfile
from django.contrib.auth import get_user_model

User = get_user_model()

class UserProfileModelTest(TestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.profile = UserProfile.objects.create(
            user=self.user,
            phone_number="1234567890",
            address="123 Test Street",
            date_of_birth="1990-01-01"
        )

    def test_profile_creation(self):
        self.assertEqual(self.profile.user, self.user)
        self.assertEqual(self.profile.phone_number, "1234567890")
        self.assertEqual(self.profile.address, "123 Test Street")
