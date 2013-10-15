from hvad.test_utils.context_managers import LanguageOverride, SettingsOverride
from hvad.test_utils.testcase import NaniTestCase
from hvad_blog.models import Entry
from django.core.urlresolvers import reverse
from hvad.test_utils.request_factory import RequestFactory

class Fixture(object):
    def create_fixtures(self):
        pass

class OneLanguage(Fixture):
    def create_fixtures(self):
        Entry.objects.language('en').create(
            is_published=True,
            title='English',
            slug='en'
        )
        super(OneLanguage, self).create_fixtures()

class TwoLanguage(Fixture):
    def create_fixtures(self):
        e = Entry.objects.language('en').create(
            is_published=True,
            title='English',
            slug='en'
        )
        
        ja = e.translate('ja')
        ja.is_published=True
        ja.title='Japanese'
        ja.slug='japanese'
        ja.save()
        super(TwoLanguage, self).create_fixtures()

class OneLanguageViewsTest(NaniTestCase, OneLanguage):

    def test_index_view(self):
        with LanguageOverride("en"):
            response = self.client.get(reverse('hvad_blog_archive_index'))
            self.assertEquals(response.status_code, 200)
            self.assertContains(response, '<a')  # links
            
        with LanguageOverride("ja"):
            response = self.client.get(reverse('hvad_blog_archive_index'))
            self.assertEquals(response.status_code, 200)
            self.assertNotContains(response, '<a') # no links       
        

class TwoLanguageViewsTest(NaniTestCase, TwoLanguage):

    def test_index_view(self):
        with LanguageOverride("en"):
            response = self.client.get(reverse('hvad_blog_archive_index'))
            self.assertEquals(response.status_code, 200)
            self.assertContains(response, '<a')  # links
            
        with LanguageOverride("ja"):
            response = self.client.get(reverse('hvad_blog_archive_index'))
            self.assertEquals(response.status_code, 200)
            self.assertContains(response, '<a') # links       
        