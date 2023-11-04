
from django.urls import path, include
from . import views
from users import views as usersViews

urlpatterns = [
    path('', usersViews.coffeeDashboard, name='coffee'),
    path('profile/', views.cprofile, name='cprofile'),
    
    path('menus/', views.menus, name='menus'),
    path('menus/category/<int:pk>/', views.coffeeitems_by_category, name='coffeeitems_by_category'),

    path('menus/category/add/', views.add_category, name='add_category'),
    path('menus/category/edit/<int:pk>/', views.edit_category, name='edit_category'),
    path('menus/category/delete/<int:pk>/', views.delete_category, name='delete_category'),
    
    path('menus/coffee/add/', views.add_coffee, name='add_coffee'),
    path('menus/coffee/edit/<int:pk>/', views.edit_coffee, name='edit_coffee'),
    path('menus/coffee/delete/<int:pk>/', views.delete_coffee, name='delete_coffee'),

    path('order_detail/<int:order_number>/', views.order_detail, name='coffee_order_detail'),
]
