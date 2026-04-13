from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from user_profile.models import Profile
from snapz.models import Snapz, Comment, SnapzImage
from scoops.models import Scoop


class SearchTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="kolade", password="test123")
        self.client.force_authenticate(user=self.user)
        Profile.objects.create(user=self.user)

    def create_test_image(self):
      return SimpleUploadedFile(
            name=f'test_image.jpg',
            content=b'fake image content',
            content_type='image/jpeg'
        )
    

    def create_new_user(self, username=None, password="test123"):
        user = User.objects.create_user(username=username, password=password)
        Profile.objects.create(user=user)
       
    
    def create_new_scoops(self, count=1, content="Yippie boy"):
        scoops = []
        for _ in range(count):
            scoops.append(Scoop.objects.create(author=self.user, content=content))
        return scoops

    def create_new_snapz(self, count=1, content="I'm tired boss"):
        snapz = []
        for _ in range(count):
            new_snapz = Snapz.objects.create(author=self.user, caption=content)
            snapz.append(new_snapz)
            SnapzImage.objects.create(snapz=new_snapz, image=self.create_test_image())
        return snapz

    def create_new_comment(self, count=1, content="Tests are torture"):
        new_snapz = self.create_new_snapz()
        comments = []
        for _ in range(count):
            comments.append(Comment.objects.create(author=self.user,
             content=content, snapz=new_snapz[0]))
        return comments

    def test_search (self):
        self.create_new_comment()
        self.create_new_snapz()
        self.create_new_scoops()
        