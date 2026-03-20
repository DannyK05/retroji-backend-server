from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Snapz, Comment, Like
from .serializers import SnapzSerializer, CommentSerializer, permission_classes


@api_view(['POST'])
@permission_classes([IsAuthenticated])

# Snapz related logic
def post_snapz (request):
    caption = request.data.get("caption")
    image = request.data.get("image")


    if not caption or not image :
        return Response({'message': "Image and caption are required"}, status=status.HTTP_400_BAD_REQUEST)
        
    try: 
        snapz = Snapz.objects.create(author=request.user, caption=caption, image=image)
    except Exception:
        return Response({'message':"Internal Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    serialized_snapz = SnapzSerializer(snapz)

    return Response({'message': "Snapz posted", 'data': {'snapz':serialized_snapz.data}}, status=status.HTTP_201_CREATED)

@api_view(['GET'])
def get_snap_by_id (request, snapz_id):
    try:
        snapz = Snapz.objects.get(id=snapz_id)
        serialized_snapz = SnapzSerializer(snapz)
        return(Response({'message': "Snapz retrieved", 'data': serialized_snapz.data}))
    except Snapz.DoesNotExist:
        return Response({'message':"Snapz not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception :
        return Response({'message':"Internal Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def get_all_snapz (request):
    snapz_list = Snapz.objects.all()
    serialized_snapz_list = SnapzSerializer(snapz_list, many=True)

    return Response({'message': "All snapz retrieved", 'data': serialized_snapz_list.data}, status=status.HTTP_200_OK)



#Comment related logic
@api_view(['POST'])
def post_comment (request):
    content = request.data.get("content")
    snapz = request.data.get("snapz")
    
    if not content :
        return Response({'message': "Comment can't be empty"}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        comment = Comment.objects.create(author=request.user, content=content, snapz = snapz)
        serialized_comment = CommentSerializer(comment)
        return Response({'message': "Comment sent", 'data': serialized_comment.data})
    except Exception :
        return Response({'message':"Internal Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

@api_view(['GET'])
def get_all_comment_by_snapz_id (request, snapz_id):

    snapz = Snapz.objects.get(id=snapz_id)
    if not snapz :
        return Response({'message': "Snapz id is not valid"}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        comment_list = Comment.objects.get(snapz_id=snapz_id)
        serialized_comment_list = CommentSerializer(comment_list, many=True)
        return Response({'message': "All comments retrieved", 'data': serialized_comment_list.data}, status=status.HTTP_200_OK)
    except Exception:
        return Response({'message':"Internal Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



#Like related logic
@ api_view(['POST'])
def like (request, snapz_id):
    pass
