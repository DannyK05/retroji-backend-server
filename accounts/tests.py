from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

# Create your tests here.
class AuthTests (APITestCase):
    def create_user(self, username, email, password):
        User.objects.create_user(
            username=username,
            email=email,
            password=password,
        )

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
        self.create_user('kolade05', 'existing@gmail.com', 'test123')
        
        url = reverse('register')
        data = {
            'username': 'kolade05',
            'email':'test@gmail.com',
            'password': "test123"
        } 

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_success(self):
        self.create_user('kolade05', 'existing@gmail.com', 'test123')

        url = reverse('login')
        data = {
            'username': 'kolade05',
            'password': 'test123'
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('user', response.data['data'])

    def test_login_nonexistent_user(self):
        self.create_user('kolade05', 'existing@gmail.com', 'test123')

        url = reverse('login')
        data = {
            'username': 'kolade',
            'password': 'test123'
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)   
        

    def test_login_wrong_password(self):
        self.create_user('kolade05', 'existing@gmail.com', 'test123')

        url = reverse('login')
        data = {
            'username': 'kolade05',
            'password': 'test124'
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)       

    def test_is_username_taken(self):
        self.create_user('kolade05', 'existing@gmail.com', 'test123')
        url = reverse('is_username_taken', kwargs={'username':'kolade05'})
    

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data["data"]["is_available"])

        url = reverse('is_username_taken', kwargs={'username':'bobby'})

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["data"]["is_available"])


    def test_logout(self):
        user = User.objects.create_user(
            username='kolade',
            password='test123'
        )

        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        url = reverse('logout')
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)