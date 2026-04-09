from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Profile, User, Follow
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
    
    

