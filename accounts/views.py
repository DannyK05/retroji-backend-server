import json
from django.contrib.auth import authenticate, login as django_login
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

@csrf_exempt
def register (request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        
        username = data.get("username")
        email = data.get("email")
        password = data.get("password")

        if not username or not password:
            return JsonResponse({"error":"Username and password are required"},status=400)
        
        if User.objects.filter(username=username).exists():
            return JsonResponse({"error": "Username already taken"}, status=400)
    
        user = User.objects.create_user(username=username, email=email, password=password)

        return JsonResponse({"message": "User Created Successfully", "user":{"id": user.id, "username":user.username}})
    
    return JsonResponse({"error": "Invalid request method"}, status=405)


@csrf_exempt
def login (request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        
        username = data.get("username")
        password = data.get("password")
    
        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None: 
            django_login(request, user)
            return JsonResponse({"message":"Login Successfully", "user":{"id": user.id, "username":user.username}})

        return JsonResponse({"message": "Invalid username or password"}, status=401)
    
    return JsonResponse({"message": "Invalid request method"}, status=405)
    
    