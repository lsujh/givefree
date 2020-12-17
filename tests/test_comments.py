from django.urls import reverse


class TestViews:
    def test_add_comment(self, create_category, create_thing, client):
        category = create_category(name='Dress')
        thing = create_thing(name="Skirt", category=category)
        comment = {'content':'документация на русском языке', 'content_object':thing, 'author':'user',
                   'email':'email@email.com'}
        kwargs = {'pk': thing.pk, 'slug': thing.slug}
        url = reverse("freestuff:thing_detail", kwargs=kwargs)
        resp = client.post(url, comment)
        assert resp.status_code == 200
        assert 'документация на русском языке'.encode() in resp.content

    def test_str(self, create_comment, create_thing, create_category):
        category = create_category(name='Dress')
        thing = create_thing(name="Skirt", category=category)
        comment = create_comment(content='документация на русском языке', content_object=thing)
        assert comment.__str__() == 'user'
