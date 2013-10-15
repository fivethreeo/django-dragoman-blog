from hvad.test_utils.context_managers import LanguageOverride, SettingsOverride
from hvad.test_utils.testcase import NaniTestCase
from hvad_blog.models import Entry, TranslationTagged
from .fixtures import *

class OneLanguageTagsTest(NaniTestCase, OneLanguage):

    def test_tags_created(self):
        with LanguageOverride("en"):
            self.en_obj.lazy_translation_getter('tags').add('some', 'english', 'tags')
        self.assertEqual(TranslationTagged.objects.filter(language_code='en').count(), 3)
        with LanguageOverride("ja"):
            self.en_obj.lazy_translation_getter('tags').add('japanese', 'othertags', 'yea')
        self.assertEqual(TranslationTagged.objects.filter(language_code='ja').count(), 3)
        self.assertEqual(TranslationTagged.objects.count(), 6)

        
        
