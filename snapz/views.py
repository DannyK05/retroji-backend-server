from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from .models import Snapz
from .serializers import SnapzSerializer


@api_view(['POST'])
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
