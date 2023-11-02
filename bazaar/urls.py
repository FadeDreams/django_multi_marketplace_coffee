from django.urls import path, include
from . import views
# from users import views as usersViews

urlpatterns = [
    path('', views.bazaar, name='bazaar'),
    path('<slug:coffee_slug>/', views.coffee_detail, name='coffee_detail'),

    path('add_to_cart/<int:coffee_id>/', views.add_to_cart, name='add_to_cart'),
    path('decrease_cart/<int:coffee_id>/', views.decrease_cart, name='decrease_cart'),
    path('delete_cart/<int:cart_id>/', views.delete_cart, name='delete_cart'),
]

