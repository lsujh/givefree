from django.contrib.sitemaps import Sitemap

from .models import Things, Category


class ThingsSitemap(Sitemap):
    priority = 0.5
    changefreq = 'daily'

    def items(self):
        return Things.objects.all()

    def lastmod(self, obj):
        return obj.updated

class CategoriesSitemap(Sitemap):
    priority = 0.5
    changefreq = 'daily'

    def items(self):
        return Category.objects.all()
