from hvad.test_utils.context_managers import LanguageOverride, SettingsOverride
from hvad.test_utils.testcase import NaniTestCase
from hvad_blog.models import Entry
from django.core.urlresolvers import reverse
from hvad.test_utils.request_factory import RequestFactory
from .fixtures import *

class OneLanguageViewsTest(NaniTestCase, OneLanguage):

    def test_index_view(self):
        with LanguageOverride("en"):
            response = self.client.get(reverse('hvad_blog_archive_index'))
            self.assertEquals(response.status_code, 200)
            self.assertContains(response, 'english')  # links
            
        with LanguageOverride("ja"):
            response = self.client.get(reverse('hvad_blog_archive_index'))
            self.assertEquals(response.status_code, 200)
            self.assertNotContains(response, 'japanese') # no links       
        

class TwoLanguageViewsTest(NaniTestCase, TwoLanguage):

    def test_index_view(self):
        with LanguageOverride("en"):
            response = self.client.get(reverse('hvad_blog_archive_index'))
            self.assertEquals(response.status_code, 200)
            self.assertContains(response, 'english')  # links
            
        with LanguageOverride("ja"):
            response = self.client.get(reverse('hvad_blog_archive_index'))
            self.assertEquals(response.status_code, 200)
            self.assertContains(response, 'japanese') # links       
        