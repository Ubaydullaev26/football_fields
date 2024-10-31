from rest_framework.test import APITestCase
from django.urls import reverse
from fields.models import FootballField
from django.contrib.auth import get_user_model
from rest_framework import status

User = get_user_model()

class FootballFieldViewTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.client.login(username='testuser', password='password123')
        self.field = FootballField.objects.create(
            owner=self.user,
            name="Test Field",
            address="123 Test Address",
            contact="1234567890",
            hourly_rate=100.0,
            latitude=40.7128,
            longitude=-74.0060,
            is_active=True
        )

    def test_field_list(self):
        url = reverse('footballfield-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_field_detail(self):
        url = reverse('footballfield-detail', args=[self.field.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], "Test Field")
