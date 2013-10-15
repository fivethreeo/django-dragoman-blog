from django.utils.translation import get_language
from django.contrib import admin
from hvad.admin import TranslatableAdmin, TranslatableTabularInline
from hvad_blog.models import Entry

class EntryAdmin(TranslatableAdmin):
    
    def __init__(self, *args, **kwargs):
        super(EntryAdmin, self).__init__(*args, **kwargs)
    
        self.prepopulated_fields = {"slug": ("title",)}
'''


class EntryTranslationInline(admin.StackedInline):
    max_num = 1
    exclude = ('language_code',)
    model = Entry.translations.related.model

    def queryset(self, request):
        queryset = super(EntryTranslationInline, self).queryset(request)
        queryset = queryset.filter(language_code=get_language())
        return queryset
        
class EntryAdmin(admin.ModelAdmin):
    
    inlines = [
        EntryTranslationInline,
    ]    
    
    def save_formset(self, request, form, formset, change):
        if formset.model ==  Entry.translations.related.model:
            formset.save(commit=False)
            for f in formset.forms:
                obj = f.instance 
                obj.language_code = get_language()
                obj.save()
            formset.save_m2m()
        else:
            super(EntryAdmin, self).save_formset(request, form, formset, change)
        
        
class EntryTranslationAdmin(admin.ModelAdmin):
    pass
    
admin.site.register(Entry.translations.related.model, EntryTranslationAdmin)
'''

admin.site.register(Entry, EntryAdmin)

