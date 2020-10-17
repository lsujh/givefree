from django.contrib.sitemaps import Sitemap

from .models import Things


class ThingsSitemap(Sitemap):
    changefreq = 'always'
    priority = 0.9

    def items(self):
        return Things.objects.all()

    def lastmod(self, obj):
        return obj.updated

