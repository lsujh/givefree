from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap

from freestuff.sitemaps import ThingsSitemap, CategoriesSitemap
from freestuff.views import robots_txt
from users.views import CustomLoginView
from blog.sitemaps import CategoriesPostSitemap, PostsSitemap
from pages.sitemaps import PagesSitemap

sitemaps = {'things': ThingsSitemap,
            'categories': CategoriesSitemap,
            'posts': PostsSitemap,
            'categories_post': CategoriesPostSitemap,
            'pages': PagesSitemap,
            }

urlpatterns = [
    path('admin/login/', CustomLoginView.as_view()),
    path('admin/', admin.site.urls),
    path('account/', include('users.urls', namespace='users')),
    path('orders/', include('orders.urls', namespace='orders')),
    path('coupons/', include('coupons.urls', namespace='coupons')),
    path('cart/', include('cart.urls', namespace='cart')),
    path('pages/', include('pages.urls', namespace='pages')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('', include('freestuff.urls', namespace='freestuff')),
    path('robots.txt', robots_txt),
    path('blog/', include('blog.urls', namespace='blog')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('search/', include('search.urls', namespace='search')),
    path('silk/', include('silk.urls', namespace='silk')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)