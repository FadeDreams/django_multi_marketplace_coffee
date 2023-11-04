from django.urls import path
from . import views

urlpatterns = [
    path('place-order/', views.place_order, name='place_order'),
    path('payments/', views.payments, name='payments'),
    path('order_complete/', views.order_complete, name='order_complete'),

    path('config/', views.stripe_config, name='config'),
    # path('create-checkout-session/', views.create_checkout_session, name='create-checkout-session'),
    path('create-checkout-session/<str:order_number>/', views.create_checkout_session, name='create-checkout-session'),

    # path('success/', views.successview, name='success'),
    # path('cancel/', views.cancelview, name='cancel'),
    path('webhook/', views.stripe_webhook, name='stripe-webhook'),
]

