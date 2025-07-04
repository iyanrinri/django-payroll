from rest_framework import status
from rest_framework.test import APITestCase
from web.models import User
from django.urls import reverse

class TestAuth(APITestCase):
    def setUp(self):
        self.name = "someone"
        self.email = "someone@test.com"
        self.password = "someone_password"
        self.user = User.objects.create(name=self.name, email=self.email)
        self.user.set_password(self.password)
        self.user.save()

    def test_login_success(self):
        url = reverse("auth-login")
        data = {
            "email": self.email,
            "password": self.password
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

    def test_login_invalid_credential(self):
        url = reverse("auth-login")
        data = {
            "email": self.email,
            "password": "wrong_password"
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('error', response.data)

    def test_logout_success(self):
        url = reverse("auth-login")
        data = {
            "email": self.email,
            "password": self.password
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

        url_logout = reverse("auth-logout")
        response = self.client.post(url_logout, headers={
            'Authorization': f"Bearer {response.data['token']}"
        }, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('message', response.data)
        self.assertEqual('Logout successfully.', response.data['message'])

    def test_logout_failed(self):
        url_logout = reverse("auth-logout")
        response = self.client.post(url_logout, headers={
            'Authorization': f"Bearer wrong_token"
        }, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('detail', response.data)
        self.assertEqual('Invalid token.', response.data['detail'])
