from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include('users.urls', namespace='users')),
    path('orders/', include('orders.urls', namespace='orders')),
    path('coupons/', include('coupons.urls', namespace='coupons')),
    path('cart/', include('cart.urls', namespace='cart')),
    path('', include('freestuff.urls', namespace='freestuff')),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)