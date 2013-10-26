from django.contrib import admin

from dragoman_blog.admin_utils import make_translation_admin
from dragoman_blog.models import Entry, EntryTranslation

SharedAdmin = make_translation_admin(EntryTranslation)

class EntryTranslationAdmin(SharedAdmin):
    exclude = ('placeholder',)
    
admin.site.register(Entry, EntryTranslationAdmin)
