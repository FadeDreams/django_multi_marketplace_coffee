from django.contrib import admin
from django.urls import path, include
from .views import home
from django.conf import settings
from django.conf.urls.static import static
from bazaar import views as baazarViews
from orders import views as ordersViews

urlpatterns = [
    path('', home, name='home'),
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('coffee/', include('coffee.urls')),
    path('bazaar/', include('bazaar.urls')),
    path('orders/', include('orders.urls')),
    # path('clients/', include('clients.urls')),
    path('cart/', baazarViews.cart, name='cart'),
    path('checkout/', baazarViews.checkout, name='checkout'),

    path('success/', ordersViews.order_complete, name='success'),
    path('cancel/', ordersViews.cancelview, name='cancel'),

    path('', include('allauth.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
