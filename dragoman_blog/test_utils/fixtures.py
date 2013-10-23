from dragoman_blog.models import Entry, EntryTranslation

class Fixture(object):
    def create_fixtures(self):
        pass

class OneLanguage(Fixture):
    def create_fixtures(self):
        entry = Entry.objects.create()
        EntryTranslation.objects.create(
            is_published=True,
            title='English',
            slug='english',
            language_code='en',
            master=entry
        )
        super(OneLanguage, self).create_fixtures()

class TwoLanguage(Fixture):
    def create_fixtures(self):
        entry = Entry.objects.create()
        EntryTranslation.objects.create(
            is_published=True,
            title='English',
            slug='english',
            language_code='en',
            master=entry
        )
        EntryTranslation.objects.create(
            is_published=True,
            title='Japanese',
            slug='japanese',
            language_code='ja',
            master=entry
        )
        super(TwoLanguage, self).create_fixtures()
