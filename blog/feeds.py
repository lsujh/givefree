from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords
from .models import Post


class LatestPostsFeed(Feed):
    title = "My blog"
    link = "/blog/"
    description = "New posts of my blog."

    def items(self):
        return Post.published.all()[:5]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        if item.description:
            return item.description
        str = '<p>Стаття вперше з\'явилась на <a href="http://things-for-your-price.pp.ua/">Практиче рукоділля</a></p>'
        return f"{truncatewords(item.body, 30)} {str}"
