from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from scoops.models import Scoop
from scoops.serializers import ScoopSerializer
from snapz.serializers import CommentSerializer, SnapzSerializer
from .models import Profile, User, Follow
from snapz.models import Comment, Snapz
from .serializers import ProfileSerializers

# Create your views here.
@api_view(["GET"])
def get_user_profile(request, user_id):

    if not user_id:
        return Response({'messsage': "user_id is required"}, status=status.HTTP_400_BAD_REQUEST)
    
    user = User.objects.filter(id=user_id).first()
    if not user:
        return Response({'message': "User not found"}, status=status.HTTP_404_NOT_FOUND)
    
    try:
        profile = Profile.objects.filter(user=user).first()
        serialized_profile = ProfileSerializers(profile, context={'request':request})
        return Response({'message': "User profile found", 'data':{'profile':serialized_profile.data}}, status=status.HTTP_200_OK)
    
    except Exception:
        return Response({'message': "Internal Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

@api_view(["GET"])
def get_user_snapz(request, user_id):

    if not user_id:
        return Response({'messsage': "user_id is required"}, status=status.HTTP_400_BAD_REQUEST)
    
    user = User.objects.filter(id=user_id).first()
    if not user:
        return Response({'message': "User not found"}, status=status.HTTP_404_NOT_FOUND)
    
    try:
        snapz = Snapz.objects.filter(user=user).first()
        serialized_snapz = SnapzSerializer(snapz, context={'request':request}, many=True)
        return Response({'message': "User's Snapz found", 'data':{'snapz':serialized_snapz.data}}, status=status.HTTP_200_OK)
    
    except Exception:
        return Response({'message': "Internal Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

@api_view(["GET"])
def get_user_scoops(request, user_id):

    if not user_id:
        return Response({'messsage': "user_id is required"}, status=status.HTTP_400_BAD_REQUEST)
    
    user = User.objects.filter(id=user_id).first()
    if not user:
        return Response({'message': "User not found"}, status=status.HTTP_404_NOT_FOUND)
    
    try:
        scoops = Scoop.objects.filter(user=user).first()
        serialized_scoops = ScoopSerializer(scoops, context={'request':request})
        return Response({'message': "User's Scoops found", 'data':{'scoops':serialized_scoops.data}}, status=status.HTTP_200_OK)
    
    except Exception:
        return Response({'message': "Internal Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["GET"])
def get_user_comments(request, user_id):

    if not user_id:
        return Response({'messsage': "user_id is required"}, status=status.HTTP_400_BAD_REQUEST)
    
    user = User.objects.filter(id=user_id).first()
    if not user:
        return Response({'message': "User not found"}, status=status.HTTP_404_NOT_FOUND)
    
    try:
        comments = Comment.objects.filter(user=user).first()
        serialized_comments = CommentSerializer(comments, context={'request':request})
        return Response({'message': "User's Comments found", 'data':{'comments':serialized_comments.data}}, status=status.HTTP_200_OK)
    
    except Exception:
        return Response({'message': "Internal Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["PUT"])
def update_user_profile(request):
    user_id = request.data.get('user_id')
    username = request.data.get('username')
    image = request.data.get('image')

    if not user_id:
        return Response({'messsage': "user_id is required"}, status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.filter(id=user_id).first()

    if not user:
        return Response({'message': "User not found"}, status=status.HTTP_404_NOT_FOUND)
    
    profile = Profile.objects.filter(user=user).first()
    try:
        if username:
            user.username = username
            user.save()

        if image:
            profile.image = image
            profile.save()
        
        profile.refresh_from_db()
        user.refresh_from_db()

        serialized_profile = ProfileSerializers(profile, context={'request':request})
        return Response({'message': "User profile updated", 'data':{'profile':serialized_profile.data}}, status=status.HTTP_200_OK)
    
    except Exception:
        return Response({'message': "Internal Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["POST"])
def follow_user_profile(request):
    user_id = request.data.get('user_id')

    if not user_id:
        return Response({'messsage': "user_id is required"}, status=status.HTTP_400_BAD_REQUEST)
    user = User.objects.filter(id=user_id).first()

    if not user:
        return Response({'message': "User not found"}, status=status.HTTP_404_NOT_FOUND)
    
    if user == request.user:
        return Response({'message': "User can't self-follow"}, status=status.HTTP_400_BAD_REQUEST)
 
    try:
        previous_following = Follow.objects.filter(following=user,follower=request.user).first()
        if previous_following:
            previous_following.delete()
            return Response({'message': f"You unfollowed {user.username}", }, status=status.HTTP_200_OK)
        else:   
            Follow.objects.create(following=user,follower=request.user)
            return Response({'message': f"You followed {user.username}", }, status=status.HTTP_200_OK)
        
    except Exception:
        return Response({'message': "Internal Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    

