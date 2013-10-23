from django.core.urlresolvers import reverse
from django.utils import translation

from dragoman_blog.test_utils.fixtures import *
from dragoman_blog.test_utils.testcase import FixtureTestCase

from dragoman_blog.models import Entry, EntryTranslation

class OneLanguageViewsTest(FixtureTestCase, OneLanguage):

    def test_index_view(self):
        with translation.override("en"):
            response = self.client.get(reverse('dragoman_blog_archive_index'))
            self.assertEquals(response.status_code, 200)
            self.assertContains(response, 'english')  # links
            
        with translation.override("ja"):
            response = self.client.get(reverse('dragoman_blog_archive_index'))
            self.assertEquals(response.status_code, 200)
            self.assertNotContains(response, 'japanese') # no links       
        

class TwoLanguageViewsTest(FixtureTestCase, TwoLanguage):

    def test_index_view(self):
        with translation.override("en"):
            response = self.client.get(reverse('dragoman_blog_archive_index'))
            self.assertEquals(response.status_code, 200)
            self.assertContains(response, 'english')  # links
            
        with translation.override("ja"):
            response = self.client.get(reverse('dragoman_blog_archive_index'))
            self.assertEquals(response.status_code, 200)
            self.assertContains(response, 'japanese') # links       
        