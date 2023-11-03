from django.urls import path
from users import views as usersViews
from . import views

urlpatterns = [
    path('', usersViews.userDashboard, name='clients'),
    path('profile/', usersViews.clprofile, name='clprofile'),
    path('my_orders/', usersViews.my_orders, name='customer_my_orders'),
    path('order_detail/<int:order_number>/', usersViews.order_detail, name='order_detail'),
]

