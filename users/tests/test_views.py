from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from users.models import UserProfile

User = get_user_model()

class UserProfileViewTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.client.login(username='testuser', password='password123')
        self.profile = UserProfile.objects.create(
            user=self.user,
            phone_number="1234567890",
            address="123 Test Street",
            date_of_birth="1990-01-01"
        )

    def test_profile_detail(self):
        url = reverse('profile-detail', args=[self.profile.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['phone_number'], "1234567890")
        self.assertEqual(response.data['address'], "123 Test Street")
