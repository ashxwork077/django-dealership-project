from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
import json

def home(request): return render(request,"home.html")
def about(request): return render(request,"About.html")
def contact(request): return render(request,"contact.html")

@csrf_exempt
@require_POST
def login_user(request):
    try:
        data=json.loads(request.body)
    except (ValueError, UnicodeDecodeError):
        return JsonResponse({"error":"Invalid JSON"},status=400)
    username=data.get("userName")
    password=data.get("password")
    if not isinstance(username,str) or not isinstance(password,str):
        return JsonResponse({"error":"userName and password required"},status=400)
    user=authenticate(request,username=username,password=password)
    if user is None:
        return JsonResponse({"status":"Failed","message":"Invalid credentials"},status=401)
    login(request,user)
    return JsonResponse({"status":"Authenticated","userName":user.username})

@csrf_exempt
@require_POST
def logout_user(request):
    if not request.user.is_authenticated:
        return JsonResponse({"status":"Failed","message":"Not logged in"},status=401)
    username=request.user.username
    logout(request)
    return JsonResponse({"status":"Logged out","userName":username})
