from pickle import GET

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import ScoopSerializer
from .models import Scoop, Like

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
    scoop_list = Scoop.objects.filter(parent=None)
    serialized_scoop_list = ScoopSerializer(scoop_list, context={'request': request}, many=True)
    return Response({'message': "All scoops retrieved", 'data': serialized_scoop_list.data}, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_all_scoops_replies_by_id(request, parent_id):
    try:
        parent_scoop = Scoop.objects.get(id=parent_id)
    except Scoop.DoesNotExist:
        return Response({'message': "Scoop not found"}, status=status.HTTP_404_NOT_FOUND)

    scoop_list = Scoop.objects.filter(parent=parent_scoop)
    serialized_scoop_list = ScoopSerializer(scoop_list, context={'request': request}, many=True)
    return Response({'message': "All replies retrieved", 'data': serialized_scoop_list.data}, status=status.HTTP_200_OK)


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

