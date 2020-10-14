from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap

from freestuff.sitemaps import ThingsSitemap

sitemaps = {'things': ThingsSitemap,}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include('users.urls', namespace='users')),
    path('orders/', include('orders.urls', namespace='orders')),
    path('coupons/', include('coupons.urls', namespace='coupons')),
    path('cart/', include('cart.urls', namespace='cart')),
    path('pages/', include('pages.urls', namespace='pages')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('', include('freestuff.urls', namespace='freestuff')),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)