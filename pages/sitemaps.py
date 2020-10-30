from django.contrib import sitemaps
from django.urls import reverse


class PagesSitemap(sitemaps.Sitemap):
    priority = 0.5
    changefreq = 'daily'


    def items(self):
        return ['pages:about', 'pages:delivery']

    def location(self, item):
        return reverse(item)