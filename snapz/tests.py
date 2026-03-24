from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.models import User
from .models import Snapz, Comment, Like
from uuid import uuid4

# Create your tests here.

class SnapzTests (APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="john_52", password="test123")
        self.client.force_authenticate(user=self.user)

    def get_test_image(self):
        
        return SimpleUploadedFile(
            name='test_image.jpg',
            content=b'fake image content',
            content_type='image/jpeg'
        )
    
    def create_snapz(self):
        snapz = Snapz.objects.create(caption="Farewell", image=self.get_test_image(), author=self.user)
        return snapz

    def create_comment(self, snapz_id, content="Nice to meet you bro"):
        comment = Comment.objects.create(author=self.user, content=content, snapz_id=snapz_id)
        return comment
    
    def test_post_snapz(self):
        url = reverse('post_snapz')
        data = {
            'caption': "Rihanna is gold",
            'image': self.get_test_image()
        }

        response = self.client.post(url, data, format='multipart')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Snapz.objects.filter(caption=data['caption']).exists())
        self.assertIn('image', response.data["data"]["snapz"])

    def test_snapz_post_with_missing_fields(self):
        url = reverse('post_snapz')
        missing_image_data = {
            'caption': "Rihanna is gold",
        }

        missing_caption_data = {
            'image': self.get_test_image()
        }

        response = self.client.post(url, missing_image_data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.post(url, missing_caption_data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)



    def test_get_snapz_by_id(self):
        snapz = self.create_snapz()

        url = reverse("get_snapz_by_id", kwargs={'snapz_id': snapz.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['data']['id'], str(snapz.id))

    def test_invalid_snapz_id(self):
        url = reverse("get_snapz_by_id", kwargs={'snapz_id': uuid4()})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_all_snapz(self):
        url = reverse("get_all_snapz")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_comment(self):
        snapz = self.create_snapz()
        url = reverse('post_comment')
        data ={'content' : "That looks really good", 'snapz_id': str(snapz.id)}
      
        response = self.client.post(url, data, format='json' )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_comment_missing_fields(self):
        snapz = self.create_snapz()
        url = reverse('post_comment')
        data_missing_snapz_id = {'content' : "That looks really good"}
        data_missing_content = {'snapz_id': str(snapz.id)}

        response = self.client.post(url, data_missing_snapz_id, format='json' )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.post(url, data_missing_content, format='json' )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_comment_invalid_snapz_id(self):
            url = reverse('post_comment')
            data = {'content': "Nice!", 'snapz_id': str(uuid4())}

            response = self.client.post(url, data, format='json')
            self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


    def test_get_all_comments_by_snapz_id(self):
        snapz = self.create_snapz()
        url = reverse('get_all_comments_by_snapz_id', kwargs={'snapz_id': snapz.id})

        self.create_comment(snapz_id=snapz.id)
        self.create_comment(snapz_id=snapz.id, content="Bro, that's great.")

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(2, Comment.objects.filter(snapz=snapz).count())
    
    def test_get_comments_invalid_snapz_id(self):
        url = reverse('get_all_comments_by_snapz_id', kwargs={'snapz_id': uuid4()})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)   
   
    def test_like_snapz(self):
        snapz = self.create_snapz()
        url = reverse('like_post')
        data={'snapz_id': str(snapz.id)}

        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Like.objects.filter(snapz=snapz).exists())
       
        response = self.client.post(url,data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(Like.objects.filter(snapz=snapz).exists())

    def test_like_invalid_snapz(self):
        url = reverse('like_post')
        data = {'snapz_id': str(uuid4())}

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        
    def test_unauthenticated_post_snapz(self):
        self.client.force_authenticate(user=None)
        url = reverse('post_snapz')
        data = {'caption': "Rihanna is gold", 'image': self.get_test_image()}

        response = self.client.post(url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)    