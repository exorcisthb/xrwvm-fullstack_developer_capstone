from django.http import JsonResponse
from django.contrib.auth import login, authenticate
import logging
import json
from django.views.decorators.csrf import csrf_exempt

logger = logging.getLogger(__name__)

@csrf_exempt
def login_user(request):
    data = json.loads(request.body)
    username = data['userName']
    password = data['password']
    user = authenticate(username=username, password=password)
    data = {"userName": username}
    if user is not None:
        login(request, user)
        data = {"userName": username, "status": "Authenticated"}
    return JsonResponse(data)

@csrf_exempt
def logout_user(request):
    from django.contrib.auth import logout
    logout(request)
    data = {"userName": ""}
    return JsonResponse(data)

def get_dealers(request):
    dealers = [
        {"id": i, "full_name": f"Dealer {i}", "city": "Austin", "address": f"{i*100} Main St", "zip": "78701", "state": "TX", "short_name": f"Dealer{i}"}
        for i in range(1, 51)
    ]
    return JsonResponse({"dealers": dealers})

def get_dealer_details(request, dealer_id):
    dealers = [
        {"id": i, "full_name": f"Dealer {i}", "city": "Austin", "address": f"{i*100} Main St", "zip": "78701", "state": "TX", "short_name": f"Dealer{i}"}
        for i in range(1, 51)
    ]
    dealer = next((d for d in dealers if d["id"] == dealer_id), None)
    if dealer:
        return JsonResponse({"dealer": dealer})
    return JsonResponse({"error": "Not found"}, status=404)

def get_dealer_reviews(request, dealer_id):
    reviews = [
        {
            "id": 1,
            "name": "John Doe",
            "dealership": dealer_id,
            "review": "Great service and friendly staff!",
            "purchase": True,
            "purchase_date": "2024-01-15",
            "car_make": "Toyota",
            "car_model": "Camry",
            "car_year": 2022,
            "sentiment": "positive"
        }
    ]
    return JsonResponse({"reviews": reviews})
