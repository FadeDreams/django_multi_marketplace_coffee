from django.urls import path
from . import views

urlpatterns = [
    path('registerUser/', views.registerUser, name='registerUser'),
    path('registerCoffee/', views.registerCoffee, name='registerCoffee'),

    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('userdashboard/', views.userDashboard, name='userDashboard'),
    path('coffeedashboard/', views.coffeeDashboard, name='coffeeDashboard'),
    path('myAccount/', views.myAccount, name='myAccount'),

    path('activate/<uidb64>/<token>/', views.activate, name='activate'),

    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('reset_password_validate/<uidb64>/<token>', views.reset_password_validate, name='reset_password_validate'),
    path('reset_password/', views.reset_password, name='reset_password'),

    # path('sendemail/', views.sendemail, name='sendemail'),
]

