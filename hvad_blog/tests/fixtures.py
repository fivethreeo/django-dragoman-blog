from hvad_blog.models import Entry

class Fixture(object):
    def create_fixtures(self):
        pass

class OneLanguage(Fixture):
    def create_fixtures(self):
        en = Entry.objects.language('en').create(
            is_published=True,
            title='English',
            slug='english'
        )
        super(OneLanguage, self).create_fixtures()

class TwoLanguage(Fixture):
    def create_fixtures(self):
        en = Entry.objects.language('en').create(
            is_published=True,
            title='English',
            slug='english'
        )
        
        ja = en.translate('ja')
        ja.is_published=True
        ja.title='Japanese'
        ja.slug='japanese'
        ja.save()
        super(TwoLanguage, self).create_fixtures()
