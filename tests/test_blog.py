import pytest

from django.urls import reverse

from blog import feeds


pytestmark = pytest.mark.django_db

class TestViews:
    def test_post_list(self, client, create_category_blog):
        categoty = create_category_blog(name='Django')
        url = reverse('blog:post_list_by_category', kwargs={'category_slug':categoty.slug})
        resp = client.get(url)
        assert resp.status_code == 200
        assert 'Категорії'.encode() in resp.content

    def test_post_detail(self, client, create_post):
        post = create_post(title='Django Mock Queries')
        date = str(post.publish.date()).split('-')
        kwargs = {'year':int(date[0]), 'month':int(date[1]), 'day':int(date[2]), 'post':post.slug}
        url = reverse('blog:post_detail', kwargs=kwargs)
        resp = client.get(url)
        assert resp.status_code == 200
        assert 'Project description'.encode() in resp.content

class TestFeed:
    def test_items(self, create_post):
        post = create_post(title='Django Mock Queries')
        latest_post = feeds.LatestPostsFeed.items(self)
        assert post in latest_post

    def test_item_title(self, create_post):
        post = create_post(title='Django Mock Queries')
        title_post = feeds.LatestPostsFeed.item_title(self, post)
        assert post.title == title_post

    def test_item_description_not(self, create_post):
        post = create_post(title='Django Mock Queries')
        description = feeds.LatestPostsFeed.item_description(self, post)
        assert 'Project description' in description

    def test_item_description(self, create_post):
        post = create_post(title='Django Mock Queries', description='Project description')
        description = feeds.LatestPostsFeed.item_description(self, post)
        assert 'Project description' in description





