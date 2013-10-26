from django.contrib import admin

from dragoman_blog.admin_utils import make_translation_admin
from dragoman_blog.models import Entry, EntryTranslation

EntryTranslationAdmin = make_translation_admin(EntryTranslation)

admin.site.register(Entry, EntryTranslationAdmin)
