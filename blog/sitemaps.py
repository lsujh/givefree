from django.contrib.sitemaps import Sitemap

from .models import Category, Post


class CategoriesPostSitemap(Sitemap):
    priority = 0.5
    changefreq = "daily"

    def items(self):
        return Category.objects.all()


class PostsSitemap(Sitemap):
    priority = 0.5
    changefreq = "daily"

    def items(self):
        return Post.published.all()

    def lastmod(self, obj):
        return obj.updated
