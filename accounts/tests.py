from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status

# Create your tests here.
class AuthTests (APITestCase):

    def test_register_success(self):
        url = reverse('register')
        data = {
            "username": "kolade",
            "email": "test@gmail.com",
            "password": "test123"
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username=data['username']).exists())

    def test_register_missing_password(self):
        url = reverse('register')
        data = {
            'username': 'kolade05',
            'email':'test@gmail.com'
        }   

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_existing_username(self):
        User.objects.create_user(
            username='kolade05',
            email='existing@gmail.com',
            password='test123'
        )

        url = reverse('register')
        data = {
            'username': 'kolade05',
            'email':'test@gmail.com',
            'password': "test123"
        } 

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"], "Username already taken")

    def test_login_success(self):
        User.objects.create_user(
            username='kolade05',
            password='test123'
        )

        url = reverse('login')
        data = {
            'username': 'kolade05',
            'password': 'test123'
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('user', response.data)

    def test_login_nonexistent_user(self):

        User.objects.create_user(
            username='kolade05',
            password='test123'
        )

        url = reverse('login')
        data = {
            'username': 'kolade',
            'password': 'test123'
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)   
        

    def test_login_wrong_password(self):

        User.objects.create_user(
            username='kolade05',
            password='test123'
        )

        url = reverse('login')
        data = {
            'username': 'kolade05',
            'password': 'test124'
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)       


    def test_logout(self):
        user = User.objects.create_user(
            username='kolade',
            password='test123'
        )

        self.client.force_login(user=user)

        url = reverse('logout')
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)