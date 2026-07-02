from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from scoops.models import Scoop
from scoops.serializers import ScoopSerializer
from snapz.serializers import CommentSerializer, SnapzSerializer
from .models import Profile, User, Follow
from snapz.models import Comment, Snapz
from .serializers import ProfileSerializer
from rest_framework.pagination import PageNumberPagination

class CustomPagination(PageNumberPagination):
    page_size=10

    def get_paginated_response(self, data, message="Success"):
        return Response({
            'message':message, 
            'data':{
                'count': self.page.paginator.count,
                'next': self.get_next_link(),
                'previous': self.get_previous_link(),
                'data': data
            }
        },status=status.HTTP_200_OK)
    
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
        serialized_profile = ProfileSerializer(profile, context={'request':request})
        return Response({'message': "User profile found", 'data': serialized_profile.data}, status=status.HTTP_200_OK)
    
    except Exception:
        return Response({'message': "Internal Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(["GET"])
def get_user_snapz(request, user_id):
    user = User.objects.filter(id=user_id).first()
    if not user:
        return Response({'message': "User not found"}, status=status.HTTP_404_NOT_FOUND)
    
    pagination = CustomPagination()
    snapz_list = Snapz.objects.filter(author=user)
    paginated_snapz_list = pagination.paginate_queryset(snapz_list, request)
    serialized_snapz = SnapzSerializer(paginated_snapz_list, context={'request': request}, many=True)
    return pagination.get_paginated_response(serialized_snapz.data, "User's Snapz found")


@api_view(["GET"])
def get_user_scoops(request, user_id):
    user = User.objects.filter(id=user_id).first()
    if not user:
        return Response({'message': "User not found"}, status=status.HTTP_404_NOT_FOUND)

    pagination = CustomPagination()
    scoops_list = Scoop.objects.filter(author=user)
    paginated_scoops_list = pagination.paginate_queryset(scoops_list, request)
    serialized_scoops = ScoopSerializer(paginated_scoops_list, context={'request': request}, many=True)
    return pagination.get_paginated_response(serialized_scoops.data, "User's Scoops found")


@api_view(["GET"])
def get_user_comments(request, user_id):
    user = User.objects.filter(id=user_id).first()
    if not user:
        return Response({'message': "User not found"}, status=status.HTTP_404_NOT_FOUND)

    pagination = CustomPagination()
    comment_list = Comment.objects.filter(author=user)
    paginated_comment_list = pagination.paginate_queryset(comment_list, request)
    serialized_comments = CommentSerializer(paginated_comment_list, context={'request': request}, many=True)
    return pagination.get_paginated_response(serialized_comments.data, "User's Comments found")

@api_view(["PUT"])
def update_user_profile(request):
    username = request.data.get('username')
    bio = request.data.get("bio")
    image = request.data.get('image')

    user = request.user
    
    profile = Profile.objects.filter(user=user).first()

    if not profile:
        return Response({'message': "Profile not found"}, status=status.HTTP_404_NOT_FOUND)

    try:
        if username:
            user.username = username
           

        if bio is not None:
            profile.bio = bio
            

        if image is not None:
            profile.image = image
           
        
        user.save()
        profile.save()
        
        profile.refresh_from_db()
        user.refresh_from_db()

        serialized_profile = ProfileSerializer(profile, context={'request':request})
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
    
    

