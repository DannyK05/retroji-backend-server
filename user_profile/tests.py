from rest_framework.test import APITestCase
from rest_framework import status
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Profile, Follow

# Create your tests here.

class UserProfileTests (APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="kolade", password="test123")
        self.client.force_authenticate(user=self.user)
        Profile.objects.create(user=self.user)

    def create_user_profile(self,user):
        profile = Profile.objects.create(user=user)
        return profile
    
    def create_new_user(self, username="baybie", password="test123"):
        user = User.objects.create_user(username=username, password=password)
        return user
    
    def get_test_image(self):
        
      return SimpleUploadedFile(
            name=f'test_image.jpg',
            content=b'fake image content',
            content_type='image/jpeg'
        )

    def test_get_user_profile(self):
        url = reverse('get_user_profile', kwargs={'user_id': self.user.id})

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)  
          

    def test_update_user_profile_username(self):
        url = reverse('update_user_profile')
        new_username = "bobby_don"
        data = {'user_id': str(self.user.id),'username': new_username }

        response = self.client.put(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['data']['profile']['user']['username'], new_username)

    
    def test_update_user_profile_image(self):
        url = reverse('update_user_profile')
        new_image = self.get_test_image()
        data = {'user_id': str(self.user.id),'image': new_image }

        response = self.client.put(url, data, format='multipart')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('test_image', response.data['data']['profile']['image'])


    def test_get_invalid_user_profile(self):
        url = reverse('get_user_profile', kwargs={'user_id': 99999})  # non-existent user id
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)   


    def test_follow_user_profile(self):
        new_user = self.create_new_user()
        url = reverse('follow_user_profile')

        data = {'user_id': str(new_user.id)}

        # follow
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK) 
        self.assertTrue(Follow.objects.filter(following=new_user, follower=self.user).exists())

        # unfollow
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK) 
        self.assertFalse(Follow.objects.filter(following=new_user, follower=self.user).exists())


    def test_cannot_follow_self(self):
        url = reverse('follow_user_profile')
        data = {'user_id': str(self.user.id)}

        response = self.client.post(url, data)

        self.assertNotEqual(response.status_code, status.HTTP_200_OK)


    def test_follow_invalid_user(self):
        url = reverse('follow_user_profile')
        data = {'user_id': 10000}

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


    def test_unauthenticated_update_profile(self):
        self.client.force_authenticate(user=None)
        url = reverse('update_user_profile')
        data = {'username': 'new_username'}

        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    