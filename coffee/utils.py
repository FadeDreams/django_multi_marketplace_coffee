from .models import Coffee

def get_coffee(request):
    return Coffee.objects.get(user=request.user)

