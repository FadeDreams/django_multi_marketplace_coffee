
from django.urls import path, include
from . import views
from users import views as usersViews

urlpatterns = [
    path('', usersViews.coffeeDashboard, name='coffee'),
    path('profile/', views.vprofile, name='vprofile'),
    
]
