from django.contrib.auth.models import User
from django.http import JsonResponse

# Create your views here.

def register (request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        if not username or not password:
            return JsonResponse({"error":"Username and password are required"},status=400)
        
        if User.objects.filter(username=username).exists():
            return JsonResponse({"error": "Username already taken"}, status=400)
    
        user = User.objects.create_user(username=username, email=email, password=password)
        return JsonResponse({"message": "User Created Successfully", "username": user.username})
    
    return JsonResponse({"error": "Invalid request method"}, status=405)