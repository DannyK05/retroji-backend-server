from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from .models import Snapz, Comment, Like, SnapzImage
from .serializers import SnapzSerializer, CommentSerializer

# Snapz related logic
@api_view(['POST'])
def post_snapz(request):
    caption = request.data.get("caption")
    images = request.data.getlist("images")

    if not caption or not images:
        return Response({'message': "Image and caption are required"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        snapz = Snapz.objects.create(author=request.user, caption=caption)
        for image in images:
            SnapzImage.objects.create(snapz=snapz, image=image)

    except Exception as e:
        print(e)
        return Response({'message': "Internal Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    serialized_snapz = SnapzSerializer(snapz, context={'request': request})
    return Response({'message': "Snapz posted", 'data': {'snapz': serialized_snapz.data}}, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def get_snapz_by_id(request, snapz_id):
    try:
        snapz = Snapz.objects.get(id=snapz_id)
        serialized_snapz = SnapzSerializer(snapz, context={'request': request})
        return Response({'message': "Snapz retrieved", 'data': serialized_snapz.data}, status=status.HTTP_200_OK)
    except Snapz.DoesNotExist:
        return Response({'message': "Snapz not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception:
        return Response({'message': "Internal Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def get_all_snapz(request):
    snapz_list = Snapz.objects.all()
    serialized_snapz_list = SnapzSerializer(snapz_list, context={'request': request}, many=True)
    return Response({'message': "All snapz retrieved", 'data': serialized_snapz_list.data}, status=status.HTTP_200_OK)


# Comment related logic
@api_view(['POST'])
def post_comment(request):
    content = request.data.get("content")
    snapz_id = request.data.get("snapz_id")

    if not content:
        return Response({'message': "Comment can't be empty"}, status=status.HTTP_400_BAD_REQUEST)

    if not snapz_id:
        return Response({'message': "snapz_id is required"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        Snapz.objects.get(id=snapz_id)
    except Snapz.DoesNotExist:
        return Response({'message': "Snapz not found"}, status=status.HTTP_404_NOT_FOUND)

    try:
        comment = Comment.objects.create(author=request.user, content=content, snapz_id=snapz_id)
        serialized_comment = CommentSerializer(comment)
        return Response({'message': "Comment sent", 'data': serialized_comment.data}, status=status.HTTP_201_CREATED)
    except Exception:
        return Response({'message': "Internal Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def get_all_comments_by_snapz_id(request, snapz_id):
    try:
        snapz = Snapz.objects.get(id=snapz_id)
    except Snapz.DoesNotExist:
        return Response({'message': "Snapz not found"}, status=status.HTTP_404_NOT_FOUND)

    comment_list = Comment.objects.filter(snapz=snapz)
    serialized_comment_list = CommentSerializer(comment_list, many=True)
    return Response({'message': "All comments retrieved", 'data': serialized_comment_list.data}, status=status.HTTP_200_OK)


# Like related logic
@api_view(['POST'])
def like(request):
    snapz_id = request.data.get('snapz_id')

    target_snapz = Snapz.objects.filter(id=snapz_id).first()
    if not target_snapz:
        return Response({'message': "Snapz not found"}, status=status.HTTP_404_NOT_FOUND)

    try:
        previous_like = Like.objects.get(author=request.user, snapz_id=snapz_id)
    except Like.DoesNotExist:
        Like.objects.create(author=request.user, snapz=target_snapz)
        return Response({'message': "You liked this Snapz"}, status=status.HTTP_201_CREATED)
    else:
        previous_like.delete()
        return Response({'message': "You unliked this Snapz"}, status=status.HTTP_200_OK)
    

@api_view(['DELETE'])
def delete_snapz(request):
    snapz_id = request.data.get("snapz_id")

    try:
        snapz = Snapz.objects.get(id=snapz_id)
    except Snapz.DoesNotExist:
        return Response({'message': "Snapz not found"}, status=status.HTTP_404_NOT_FOUND)

    if snapz.author != request.user:
        return Response({'message': "You can't delete someone else's snapz"}, status=status.HTTP_403_FORBIDDEN)

    snapz.delete()
    return Response({'message': "Snapz deleted"}, status=status.HTTP_200_OK)

@api_view(['DELETE'])
def delete_comment(request):
    comment_id = request.data.get("comment_id")

    try:
        comment = Comment.objects.get(id=comment_id)
    except Comment.DoesNotExist:
        return Response({'message': "Comment not found"}, status=status.HTTP_404_NOT_FOUND)

    if comment.author != request.user:
        return Response({'message': "You can't delete someone else's comment"}, status=status.HTTP_403_FORBIDDEN)

    comment.delete()
    return Response({'message': "Comment deleted"}, status=status.HTTP_200_OK)