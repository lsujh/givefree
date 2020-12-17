import pytest

from badwordfilter import models, views

pytestmark = pytest.mark.django_db

class TestModel:
    def test_save_unicode(self):
        word = models.Slang.objects.create(word='word')
        assert models.Slang.objects.count() == 1
        assert word.__unicode__() == 'word'


class TestPymorphyProc:
    def test_wrap(self):
        models.Slang.objects.create(word='text')
        word = views.PymorphyProc.wrap('text', wrap=('<', '/>'))
        assert word == '<text/>'

    def test_replace(self):
        models.Slang.objects.create(word='text')
        word = views.PymorphyProc.replace('text', '***')
        assert word == '***'

    def test_test(self):
        models.Slang.objects.create(word='text')
        models.Slang.objects.create(word='word')
        word = views.PymorphyProc.test('text word')
        assert word == 2

class TestRegexpProc:
    def test_wrap(self):
        word = views.RegexpProc.wrap('te')
        assert word == 'te'
        word = views.RegexpProc.wrap('ххуйхх', wrap=('<', '/>'))
        assert word == '<ххуйхх/>'

    def test_test(self):
        word = views.RegexpProc.test('ххуйхх')
        assert word
