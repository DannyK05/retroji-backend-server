from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from user_profile.models import Profile
from snapz.models import Snapz, Comment
from scoops.models import Scoop
from snapz.serializers import SnapzSerializer, CommentSerializer
from scoops.serializers import ScoopSerializer
from user_profile.serializers import ProfileSerializer


# Create your views here.
@api_view(['GET'])
def search(request):
    query = request.query_params.get('q')

    if not query :
        return Response({'message': "Search query is required"}, status=status.HTTP_400_BAD_REQUEST)
    
    snapz = Snapz.objects.filter(caption__icontains=query)
    scoops = Scoop.objects.filter(content__icontains=query)
    comments = Comment.objects.filter(content__icontains=query)
    profiles = Profile.objects.filter(user__username_icontains=query)
    
    return Response({
        'message': "Search results",
        'data':{
            'snapz': SnapzSerializer(snapz, many=True, context={'request': request}).data,
            'scoops': ScoopSerializer(scoops, many=True, context={'request': request}).data,
            'comments': CommentSerializer(comments, many=True, context={'request': request}).data,
            'profiles': ProfileSerializer(profiles, many=True, context={'request': request}).data,
        }
    }, status=status.HTTP_200_OK)