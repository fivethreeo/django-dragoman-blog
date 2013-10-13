from django.contrib import admin
from hvad.admin import TranslatableAdmin, TranslatableTabularInline
from hvad_blog.models import Entry

class EntryAdmin(TranslatableAdmin):
    
    def __init__(self, *args, **kwargs):
        super(EntryAdmin, self).__init__(*args, **kwargs)
    
        self.prepopulated_fields = {"slug": ("title",)}
    
admin.site.register(Entry, EntryAdmin)

