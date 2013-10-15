from hvad_blog.models import Entry

class Fixture(object):
    def create_fixtures(self):
        pass

class OneLanguage(Fixture):
    def create_fixtures(self):
        self.en_obj = Entry.objects.language('en').create(
            is_published=True,
            title='English',
            slug='english'
        )
        super(OneLanguage, self).create_fixtures()

class TwoLanguage(Fixture):
    def create_fixtures(self):
        self.en_obj = Entry.objects.language('en').create(
            is_published=True,
            title='English',
            slug='english'
        )
        
        self.ja_obj = self.en_obj.translate('ja')
        self.ja_obj.is_published=True
        self.ja_obj.title='Japanese'
        self.ja_obj.slug='japanese'
        self.ja_obj.save()
        super(TwoLanguage, self).create_fixtures()
