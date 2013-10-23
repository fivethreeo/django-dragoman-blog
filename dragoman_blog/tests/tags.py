from django.utils import translation

from dragoman_blog.test_utils.fixtures import *
from dragoman_blog.test_utils.testcase import FixtureTestCase

from dragoman_blog.models import Entry, EntryTranslation, TranslationTagged

class TwoLanguageTagsTest(FixtureTestCase, TwoLanguage):
    
    def assert_tags_equal(self, qs, tags, sort=True, attr="name"):
            got = [getattr(obj, attr) for obj in qs]
            if sort:
                got.sort()
                tags.sort()
            self.assertEqual(got, tags)
            
    def setUp(self):
        super(TwoLanguageTagsTest, self).setUp()
        en = EntryTranslation.objects.get(language_code='en')
        en.tags.add('some', 'english', 'tags')    
        ja = EntryTranslation.objects.get(language_code='ja')
        ja.tags.add('ooh', 'japanese', 'othertags')    
            
    def test_tags_created(self):
        self.assertEqual(TranslationTagged.objects.filter(language_code='en').count(), 3)
        self.assertEqual(TranslationTagged.objects.filter(language_code='ja').count(), 3)
        self.assertEqual(TranslationTagged.objects.count(), 6)

    def test_tags_get_attr(self):
        en = EntryTranslation.objects.get(language_code='en')
        ja = EntryTranslation.objects.get(language_code='ja')
        self.assertEqual(list(en.tags.names()).sort(), [u'english', u'some', u'tags'].sort())   
        self.assertEqual(list(ja.tags.names()).sort(), [u'ooh', u'japanese', u'othertags'].sort())       

    def test_tags_get_api(self):
        with translation.override("en"):
            self.assert_tags_equal(TranslationTagged.tags_for(EntryTranslation),
                 [u'english', u'some', u'tags'])
            
        with translation.override("ja"):     
            self.assert_tags_equal(TranslationTagged.tags_for(EntryTranslation),
                 [u'ooh', u'japanese', u'othertags'])
        
        
        
