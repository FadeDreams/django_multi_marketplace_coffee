
from coffee.models import Coffee
from django.conf import settings
from .models import UserProfile


def get_coffee(request):
    try:
        coffee = Coffee.objects.get(user=request.user)
    except:
        coffee = None
    return dict(coffee=coffee)
