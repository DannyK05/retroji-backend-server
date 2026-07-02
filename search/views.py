from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from user_profile.models import Profile
from snapz.models import Snapz, Comment
from scoops.models import Scoop
from snapz.serializers import SnapzSerializer, CommentSerializer
from scoops.serializers import ScoopSerializer
from user_profile.serializers import ProfileSerializer
from rest_framework.pagination import PageNumberPagination

class CustomPagination(PageNumberPagination):
    page_size=10

    def get_paginated_response(self, data):
        return {
                'count': self.page.paginator.count,
                'next': self.get_next_link(),
                'previous': self.get_previous_link(),
                'data': data
            }
       
    
# Create your views here.
@api_view(['GET'])
def search(request):
    query = request.query_params.get('q')

    if not query :
        return Response({'message': "Search query is required"}, status=status.HTTP_400_BAD_REQUEST)
    
    pagination = CustomPagination()
    snapz_list = Snapz.objects.filter(caption__icontains=query)
    scoops_list = Scoop.objects.filter(content__icontains=query)
    comment_list = Comment.objects.filter(content__icontains=query)
    profile_list = Profile.objects.filter(user__username__icontains=query)

    paginated_snapz_list = pagination.paginate_queryset(snapz_list, request)
    paginated_scoops_list = pagination.paginate_queryset(scoops_list, request)
    paginated_comment_list = pagination.paginate_queryset(comment_list, request)
    paginated_profile_list = pagination.paginate_queryset(profile_list, request)


    
    return Response({
        'message': "Search results",
        'data':{
            'snapz': pagination.get_paginated_response(SnapzSerializer(paginated_snapz_list, many=True, context={'request': request}).data),
            'scoops': pagination.get_paginated_response(ScoopSerializer(paginated_scoops_list, many=True, context={'request': request}).data),
            'comments': pagination.get_paginated_response(CommentSerializer(paginated_comment_list, many=True, context={'request': request}).data),
            'profiles': pagination.get_paginated_response(ProfileSerializer(paginated_profile_list, many=True, context={'request': request}).data),
        }
    }, status=status.HTTP_200_OK)