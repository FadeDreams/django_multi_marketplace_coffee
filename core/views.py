from coffee.models import Coffee
from coffee.models import UserProfile
from django.db.models import F, ExpressionWrapper, FloatField
from django.shortcuts import render
from coffee.models import Coffee
import math


def calculate_haversine(lat1, lon1, lat2, lon2):
    # Convert latitude and longitude from degrees to radians
    lat1 = float(lat1)
    lon1 = float(lon1)
    lat2 = float(lat2)
    lon2 = float(lon2)
    
    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    
    # Radius of the Earth in kilometers (mean value)
    radius = 6371
    
    # Calculate the distance in kilometers
    distance = radius * c
    
    return distance


def home(request):
    if request.user.is_authenticated:
        user = request.user
        try:
            user_profile = UserProfile.objects.get(user=user)
            user_latitude = user_profile.latitude
            user_longitude = user_profile.longitude
        except UserProfile.DoesNotExist:
            user_latitude = None
            user_longitude = None
    else:
        user_latitude = None
        user_longitude = None

    coffee_name = request.GET.get('coffee_name', '')

    # Filter coffee objects that contain the specified coffee_name
    coffees = Coffee.objects.filter(
        is_approved=True,
        user__is_active=True,
        coffee_name__icontains=coffee_name
    ).annotate(
        coffee_latitude=F('user__userprofile__latitude'),
        coffee_longitude=F('user__userprofile__longitude')
    ).order_by('created_at')

    nearest_coffees = []
    min_distances = [float('inf')] * 5

    for coffee in coffees:
        latitude = coffee.coffee_latitude
        longitude = coffee.coffee_longitude

        if user_latitude is not None and user_longitude is not None and latitude is not None and longitude is not None:
            distance = calculate_haversine(user_latitude, user_longitude, latitude, longitude)

            # Check if this coffee is closer than any of the current nearest coffees
            for i in range(5):
                if distance < min_distances[i]:
                    min_distances.insert(i, distance)
                    min_distances.pop()
                    nearest_coffees.insert(i, coffee)
                    nearest_coffees.pop()

    print('nearest_coffees', nearest_coffees)
    context = {
        'user_latitude': user_latitude,
        'user_longitude': user_longitude,
        'nearest_coffees': nearest_coffees,
        'coffee_name': coffee_name,
    }
    return render(request, 'home.html', context)





