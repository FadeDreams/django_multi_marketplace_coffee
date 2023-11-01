from django.urls import path
from . import views

urlpatterns = [
    path('registerUser/', views.registerUser, name='registerUser'),
    path('registerCoffee/', views.registerCoffee, name='registerCoffee'),

    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('dashboard/', views.userDashboard, name='userDashboard'),
    path('dashboard/', views.coffeeDashboard, name='coffeeDashboard'),
    path('myAccount/', views.myAccount, name='myAccount'),
]

