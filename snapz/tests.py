from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from uuid import uuid4
from django.contrib.auth.models import User
from .models import Snapz, SnapzImage, Comment, Like


# Create your tests here.

class SnapzTests (APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="john_52", password="test123")
        self.client.force_authenticate(user=self.user)

    def get_test_image(self, count=1):
        
        files = []
        for i in range(count):
            files.append(SimpleUploadedFile(
            name=f'test_image_{i}.jpg',
            content=b'fake image content',
            content_type='image/jpeg'
        ))
        if (len(files) > 1):
            return files
        else:
            return files[0]
        
    
    def create_snapz(self):
        snapz = Snapz.objects.create(caption="Farewell",  author=self.user)
        SnapzImage.objects.create(snapz=snapz, image=self.get_test_image())
        return snapz

    def create_comment(self, snapz_id, content="Nice to meet you bro"):
        comment = Comment.objects.create(author=self.user, content=content, snapz_id=snapz_id)
        return comment
    
    def test_post_snapz_with_single_image(self):
        url = reverse('post_snapz')
        data = {
            'caption': "Rihanna is gold",
            'images': self.get_test_image()
        }

        response = self.client.post(url, data, format='multipart')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Snapz.objects.filter(caption=data['caption']).exists())
        self.assertIn('images', response.data["data"]["snapz"])

    def test_post_snapz_with_multiple_image(self):
        image_count = 3
        url = reverse('post_snapz')
        data = {
            'caption': "Rihanna is gold",
            'images': self.get_test_image(image_count)
        }

        response = self.client.post(url, data, format='multipart')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Snapz.objects.filter(caption=data['caption']).exists())
        self.assertIn('images', response.data["data"]["snapz"])  
        self.assertEqual(len(response.data['data']['snapz']['images']), image_count)
        

    def test_snapz_post_with_missing_fields(self):
        url = reverse('post_snapz')
        missing_image_data = {
            'caption': "Rihanna is gold",
        }

        missing_caption_data = {
            'images': self.get_test_image()
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

        # test like
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Like.objects.filter(snapz=snapz).exists())
       
        # To test if is_liked prop is updated
        get_url = reverse('get_snapz_by_id', kwargs={'snapz_id': snapz.id})
        get_response = self.client.get(get_url)
        self.assertTrue(get_response.data['data']['is_liked'])

        # test unlike
        response = self.client.post(url,data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(Like.objects.filter(snapz=snapz).exists())

        # To test if is_liked prop is updated
        get_response = self.client.get(get_url)
        self.assertFalse(get_response.data['data']['is_liked'])

    def test_like_invalid_snapz(self):
        url = reverse('like_post')
        data = {'snapz_id': str(uuid4())}

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


        
    def test_unauthenticated_post_snapz(self):
        self.client.force_authenticate(user=None)
        url = reverse('post_snapz')
        data = {'caption': "Rihanna is gold", 'images': self.get_test_image()}

        response = self.client.post(url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)    

    def test_delete_snapz(self):
        snapz = self.create_snapz()
        data = {'snapz_id': str(snapz.id)}
        url = reverse('delete_snapz')

        response = self.client.delete(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(Snapz.objects.filter(id=snapz.id).exists())
    
    def test_delete_comment(self):
        snapz = self.create_snapz()
        comment = self.create_comment(snapz_id=snapz.id)
        data = {'comment_id': str(comment.id)}
        url = reverse('delete_comment')

        response = self.client.delete(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(Comment.objects.filter(id=comment.id).exists())