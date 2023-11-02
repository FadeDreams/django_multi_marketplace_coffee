from django.shortcuts import render
from coffee.models import Coffee


def home(request):
    coffees = Coffee.objects.filter(is_approved=True, user__is_active=True).order_by('created_at')
    context = {
        'coffees': coffees,
    }
    return render(request, 'home.html', context)

