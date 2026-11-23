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

def get_dealer_reviews(request, dealer_id):
    if request.method != "GET":
        return JsonResponse({"error":"Method not allowed"},status=405)
    # Explicitly labeled sample data until the dealership reviews database is connected.
    reviews = {
        1: [
            {"id": 101, "dealership": 1, "name": "Aarav Patel", "purchase": True, "review": "Helpful staff and a smooth car buying experience.", "sentiment": "positive"},
            {"id": 102, "dealership": 1, "name": "Neha Rao", "purchase": False, "review": "The team answered my questions clearly.", "sentiment": "positive"}
        ],
        2: [
            {"id": 201, "dealership": 2, "name": "Kabir Shah", "purchase": True, "review": "Good selection, but delivery took longer than expected.", "sentiment": "neutral"}
        ]
    }
    return JsonResponse({"dealer_id": dealer_id, "sample_data": True, "reviews": reviews.get(dealer_id, [])})

def get_all_dealers(request):
    if request.method != "GET":
        return JsonResponse({"error":"Method not allowed"},status=405)
    # Demonstration records; replace with database-backed dealership records for production.
    dealers = [
        {"id": 1, "full_name": "DriveWise Pune Central", "short_name": "DW Pune", "city": "Pune", "state": "Maharashtra", "address": "Sample Showroom, Pune, India"},
        {"id": 2, "full_name": "DriveWise Mumbai West", "short_name": "DW Mumbai", "city": "Mumbai", "state": "Maharashtra", "address": "Sample Showroom, Mumbai, India"}
    ]
    return JsonResponse({"sample_data": True, "dealers": dealers})

def get_dealer_by_id(request, dealer_id):
    if request.method != "GET":
        return JsonResponse({"error": "Method not allowed"}, status=405)
    # Coursework sample data; production should query the dealer database.
    dealers = {
        1: {"id": 1, "full_name": "DriveWise Pune Central", "short_name": "DW Pune", "city": "Pune", "state": "Maharashtra", "address": "Sample Showroom, Pune, India"},
        2: {"id": 2, "full_name": "DriveWise Mumbai West", "short_name": "DW Mumbai", "city": "Mumbai", "state": "Maharashtra", "address": "Sample Showroom, Mumbai, India"}
    }
    dealer = dealers.get(dealer_id)
    if dealer is None:
        return JsonResponse({"error": "Dealer not found"}, status=404)
    return JsonResponse({"sample_data": True, "dealer": dealer})

def get_dealers_by_state(request, state):
    if request.method != "GET":
        return JsonResponse({"error": "Method not allowed"}, status=405)
    sample_dealers = [
        {"id": 3, "full_name": "Prairie Auto Kansas City", "short_name": "Prairie Auto", "city": "Kansas City", "state": "Kansas", "address": "Sample Address, Kansas City, KS, USA"},
        {"id": 4, "full_name": "Sunflower Motors Wichita", "short_name": "Sunflower Motors", "city": "Wichita", "state": "Kansas", "address": "Sample Address, Wichita, KS, USA"},
    ]
    matches = [dealer for dealer in sample_dealers if dealer["state"].casefold() == state.casefold()]
    return JsonResponse({"sample_data": True, "state": state, "dealers": matches})

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

@login_required(login_url="/admin/login/")
def dealers_page(request):
    dealers = [
        {"id": 1, "full_name": "DriveWise Pune Central", "city": "Pune", "state": "Maharashtra"},
        {"id": 2, "full_name": "DriveWise Mumbai West", "city": "Mumbai", "state": "Maharashtra"},
        {"id": 3, "full_name": "Prairie Auto Kansas City", "city": "Kansas City", "state": "Kansas"},
        {"id": 4, "full_name": "Sunflower Motors Wichita", "city": "Wichita", "state": "Kansas"},
    ]
    return render(request, "dealers.html", {"dealers": dealers})

def get_all_car_makes(request):
    if request.method != "GET":
        return JsonResponse({"error": "Method not allowed"}, status=405)
    # Demonstration catalog, not retrieved from the course's external cars API.
    makes = [
        {"id": 1, "name": "Toyota", "models": [{"id": 101, "name": "Corolla"}, {"id": 102, "name": "Camry"}]},
        {"id": 2, "name": "Honda", "models": [{"id": 201, "name": "Civic"}, {"id": 202, "name": "Accord"}]},
        {"id": 3, "name": "Ford", "models": [{"id": 301, "name": "Mustang"}, {"id": 302, "name": "Escape"}]}
    ]
    return JsonResponse({"sample_data": True, "car_makes": makes})

def analyze_review(request):
    if request.method != "GET":
        return JsonResponse({"error": "Method not allowed"}, status=405)
    review = request.GET.get("text", "")
    if not review.strip():
        return JsonResponse({"error": "Review text is required"}, status=400)
    positive = {"fantastic", "excellent", "great", "amazing", "good", "helpful", "wonderful"}
    negative = {"bad", "terrible", "poor", "awful", "horrible", "disappointing"}
    import re
    words = set(re.findall(r"[a-z]+", review.lower()))
    score = len(words & positive) - len(words & negative)
    sentiment = "positive" if score > 0 else "negative" if score < 0 else "neutral"
    return JsonResponse({"review": review, "sentiment": sentiment, "analysis_method": "demo_keyword_rules"})
