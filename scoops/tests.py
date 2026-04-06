from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from .models import Scoop, Like
from django.urls import reverse

# Create your tests here.
class ScoopTests (APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="john_52", password="test123")
        self.client.force_authenticate(user=self.user)
    
    def get_test_scoop(self, parent=None, content="Hey there, newbie"):
        scoop = Scoop.objects.create(author=self.user, content=content, parent_id=parent)
        return scoop

    def test_post_scoop(self):
        url = reverse('post_scoops')
        data = {'content': "My bread is stale"}
        
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_scoop_reply(self):
        url = reverse('post_scoops')
        parent_scoop = self.get_test_scoop()
        data = {'content': "My bread is stale", 'parent_id': str(parent_scoop.id)}
        
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['data']['scoop']['parent'], str(parent_scoop.id))
        

    def test_post_scoop_missing_content_field(self):
        url = reverse('post_scoops')
        data = {}

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_like_scoop(self):
        url = reverse('like_scoops')
        scoop = self.get_test_scoop()
        data = {'scoop': scoop.id}

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Like.objects.filter(scoop=scoop).exists())

        unlike_response = self.client.post(url, data, format='json')
        self.assertEqual(unlike_response.status_code, status.HTTP_200_OK)
        self.assertFalse(Like.objects.filter(scoop=scoop).exists())

    def test_get_all_scoops(self):
        url = reverse('get_all_scoops')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        

    def test_get_all_scoops_by_id(self):
        scoop = self.get_test_scoop()
        url = reverse('get_all_scoops_by_id', kwargs={'parent_id':scoop.id})
        
        self.get_test_scoop(scoop.id, content="I'm not a newbie")
        self.get_test_scoop(scoop.id, content="Stop hating")

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data['data']),2)
    
    def test_unauthenticated_post_scoops(self):
        self.client.force_authenticate(user=None)
        url = reverse('post_scoops')
        data = {'content': "My bread is stale"}

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)    