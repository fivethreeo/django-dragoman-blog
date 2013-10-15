from hvad.test_utils.context_managers import LanguageOverride, SettingsOverride
from hvad.test_utils.testcase import NaniTestCase
from hvad_blog.models import Entry, TranslationTagged
from .fixtures import *

class TwoLanguageTagsTest(NaniTestCase, TwoLanguage):
    
    def assert_tags_equal(self, qs, tags, sort=True, attr="name"):
            got = [getattr(obj, attr) for obj in qs]
            if sort:
                got.sort()
                tags.sort()
            self.assertEqual(got, tags)
            
    def setUp(self):
        super(TwoLanguageTagsTest, self).setUp()
        en = Entry.objects.language('en').get(pk=1)
        en.lazy_translation_getter('tags').add('some', 'english', 'tags')    
        ja = Entry.objects.language('ja').get(pk=1)
        ja.lazy_translation_getter('tags').add('ooh', 'japanese', 'othertags')    
            
    def test_tags_created(self):
        self.assertEqual(TranslationTagged.objects.filter(language_code='en').count(), 3)
        self.assertEqual(TranslationTagged.objects.filter(language_code='ja').count(), 3)
        self.assertEqual(TranslationTagged.objects.count(), 6)

    def test_tags_get_attr(self):
        en = Entry.objects.language('en').get(pk=1)
        ja = Entry.objects.language('ja').get(pk=1)        
        self.assertEqual(list(en.lazy_translation_getter('tags').names()).sort(), [u'english', u'some', u'tags'].sort())   
        self.assertEqual(list(ja.lazy_translation_getter('tags').names()).sort(), [u'ooh', u'japanese', u'othertags'].sort())       

    def test_tags_get_api(self):
        with LanguageOverride("en"):
            self.assert_tags_equal(TranslationTagged.tags_for(Entry.translations.related.model),
                 [u'english', u'some', u'tags'])
            
        with LanguageOverride("ja"):     
            self.assert_tags_equal(TranslationTagged.tags_for(Entry.translations.related.model),
                 [u'ooh', u'japanese', u'othertags'])
        
        
        
