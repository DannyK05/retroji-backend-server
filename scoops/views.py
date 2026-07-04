from rest_framework.pagination import PageNumberPagination
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import ScoopSerializer
from .models import Scoop, Like

class CustomPagination(PageNumberPagination):
    page_size=20
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

@api_view(['POST'])
def post_scoops(request):
    content = request.data.get('content')
    parent_id = request.data.get('parent_id')

    if not content:
        return Response({'message': "Content is required"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        scoop = Scoop.objects.create(author=request.user, content=content, parent_id=parent_id)
    except Exception:
        return Response({'message': "Internal Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    serialized_scoop = ScoopSerializer(scoop, context={'request': request})
    return Response({'message': "Scoop posted", 'data': {'scoop': serialized_scoop.data}}, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def like_scoops(request):
    scoop_id = request.data.get('scoop_id')

    if not scoop_id:
        return Response({'message': "Scoop is required"}, status=status.HTTP_400_BAD_REQUEST)

    scoop = Scoop.objects.filter(id=scoop_id).first()
    if not scoop:
        return Response({'message': "Scoop not found"}, status=status.HTTP_404_NOT_FOUND)

    try:
        previous_like = Like.objects.filter(author=request.user, scoop=scoop).first()
        if not previous_like:
            Like.objects.create(author=request.user, scoop=scoop)
            return Response({'message': "You liked this scoop"}, status=status.HTTP_201_CREATED)
        else:
            previous_like.delete()
            return Response({'message': "You unliked this scoop"}, status=status.HTTP_200_OK)
    except Exception:
        return Response({'message': "Internal Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def get_all_scoops(request):
    pagination = CustomPagination()
    scoop_list = Scoop.objects.filter(parent=None)
    paginated_scoop_list = pagination.paginate_queryset(scoop_list, request)
    serialized_scoop_list = ScoopSerializer(paginated_scoop_list, context={'request': request}, many=True)
    return pagination.get_paginated_response(serialized_scoop_list.data, "All scoops retrieved")


@api_view(['GET'])
def get_all_scoops_replies_by_id(request, parent_id):
    try:
        parent_scoop = Scoop.objects.get(id=parent_id)
    except Scoop.DoesNotExist:
        return Response({'message': "Scoop not found"}, status=status.HTTP_404_NOT_FOUND)
    
    pagination = CustomPagination()
    scoop_list = Scoop.objects.filter(parent=parent_scoop)
    paginated_scoop_list = pagination.paginate_queryset(scoop_list, request)
    serialized_scoop_list = ScoopSerializer(paginated_scoop_list, context={'request': request}, many=True)
    return pagination.get_paginated_response(serialized_scoop_list.data,"All replies retrieved")


@api_view(['DELETE'])
def delete_scoops(request):
    scoop_id = request.data.get("scoop_id")

    try:
        scoop = Scoop.objects.get(id=scoop_id)
    except Scoop.DoesNotExist:
        return Response({'message': "Scoop not found"}, status=status.HTTP_404_NOT_FOUND)

    if scoop.author != request.user:
        return Response({'message': "You can't delete someone else's scoop"}, status=status.HTTP_403_FORBIDDEN)

    scoop.delete()
    return Response({'message': "Scoop deleted"}, status=status.HTTP_200_OK)

