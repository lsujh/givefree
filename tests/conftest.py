import pytest
import uuid
from selenium import webdriver
from datetime import timedelta

from django.utils import timezone

from freestuff.models import Category, Things
from blog.models import Category as cat_blog, Post
from comments.models import Comment
from coupons.models import Coupon
from likes.models import LikeDislike
from orders.models import Order


@pytest.fixture
def browser():
    browser = webdriver.Chrome()
    yield browser
    browser.quit()

@pytest.fixture
def test_password():
    return 'password'

@pytest.fixture
def create_user(db, django_user_model, test_password):
    def make_user(**kwargs):
        kwargs['password'] = test_password
        kwargs['id'] = str(uuid.uuid4())
        kwargs['email_confirm'] = True
        kwargs['first_name'] = 'first_name'
        kwargs['last_name'] = 'last_name'
        return django_user_model.objects.create_user(**kwargs)
    return make_user

@pytest.fixture
def auto_login_user(db, client, create_user, test_password):
    def make_auto_login(user=None):
        if user is None:
            user = create_user(email='super@test.com')
        client.login(email=user.email, password=test_password)
        return client, user
    return make_auto_login

@pytest.fixture
def create_category(db):
    def make_category(**kwargs):
        kwargs['slug'] = 'dress'
        return Category.objects.create(**kwargs)
    return make_category

@pytest.fixture
def create_thing(db, create_user):
    def make_thing(**kwargs):
        kwargs['slug'] = 'skirt'
        kwargs['keywords'] = ['word']
        kwargs['quantity'] = 1
        kwargs['owner'] = create_user(email='email@email.com')
        return Things.objects.create(**kwargs)
    return make_thing

@pytest.fixture
def create_category_blog(db):
    def make_category(**kwargs):
        kwargs['slug'] = 'django'
        return cat_blog.objects.create(**kwargs)
    return make_category

@pytest.fixture
def create_post(db, create_user, create_category_blog):
    def make_post(**kwargs):
        kwargs['author'] = create_user(email='email@email.com', email_confirm=True)
        kwargs['category'] = create_category_blog(name='Django')
        kwargs['slug'] = 'django_mock_queries'
        kwargs['keywords'] = ['word']
        kwargs['body'] = 'Project description'
        kwargs['status'] = 'published'
        kwargs['publish'] = timezone.now()
        return Post.objects.create(**kwargs)
    return make_post

@pytest.fixture
def create_comment(db):
    def make_comment(**kwargs):
        kwargs['author'] = 'user'
        kwargs['email'] = 'user@email.com'
        return Comment.objects.create(**kwargs)
    return make_comment

@pytest.fixture
def create_coupon(db):
    def make_coupon(**kwargs):
        kwargs['valid_from'] = timezone.now() - timedelta(days=1)
        kwargs['valid_to'] = timezone.now() + timedelta(days=1)
        kwargs['active'] = True
        return Coupon.objects.create(**kwargs)
    return make_coupon

@pytest.fixture
def create_like(db, create_thing, create_category, create_user, create_comment):
    def make_like(**kwargs):
        kwargs['vote'] = 0
        # kwargs['user'] = create_user(email='user@email.com', email_confirm=True)
        category = create_category(name='Dress')
        thing = create_thing(name="Skirt", category=category)
        comment = create_comment(content='документация на русском языке', content_object = thing)
        kwargs['content_object'] = comment
        return LikeDislike.objects.create(**kwargs)
    return make_like

@pytest.fixture
def create_order(db):
    def make_order(**kwargs):
        kwargs['first_name'] = 'Ivan'
        kwargs['last_name'] = 'Ivanov'
        kwargs['email'] = 'user@email.com'
        kwargs['phone'] = 9999999999
        kwargs['city'] = 'Kiev'
        kwargs['shipping'] = 'Ukrposhta'
        kwargs['status'] = 'Created'
        return Order.objects.create(**kwargs)
    return make_order
