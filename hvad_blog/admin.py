from django.utils.translation import get_language
from django.contrib import admin
from hvad.admin import TranslatableAdmin, TranslatableTabularInline
from hvad_blog.models import Entry
from django.utils.encoding import force_unicode
from django.utils.html import escape
from django.http import Http404, HttpResponseRedirect
from django.core.urlresolvers import reverse
from functools import update_wrapper
from django.contrib.admin.util import unquote


class EntryAdmin(TranslatableAdmin):
    
    def __init__(self, *args, **kwargs):
        super(EntryAdmin, self).__init__(*args, **kwargs)
    
        self.prepopulated_fields = {"slug": ("title",)}
'''

        
class EntryTranslationAdmin(admin.ModelAdmin):
    
    def change_view(self, request, object_id, form_url='', extra_context=None):
        "The 'change' admin view for this model."
        model = self.model
        opts = model._meta

        obj = self.get_object(request, unquote(object_id))

        if not self.has_change_permission(request, obj):
            raise PermissionDenied

        if obj is None:
            raise Http404(_('%(name)s object with primary key %(key)r does not exist.') % {'name': force_unicode(opts.verbose_name), 'key': escape(object_id)})
        return HttpResponseRedirect(reverse('admin:hvad_blog_entry_change', args=[obj.master.pk])+'?language='+obj.language_code)

class EntryTranslationInline(admin.StackedInline):
    max_num = 1
    exclude = ('language_code',)
    model = Entry.translations.related.model

    def queryset(self, request):
        queryset = super(EntryTranslationInline, self).queryset(request)
        queryset = queryset.filter(language_code=get_language())
        return queryset
        
class EntryAdmin(admin.ModelAdmin):
    
    def __init__(self, model, admin_site):
        super(EntryAdmin, self).__init__(model, admin_site)
        self._translation_admin = self.translation[1](self.translation[0], admin_site)
        self._translation_model = self.translation[0]
                    
    translation = (Entry.translations.related.model, EntryTranslationAdmin)
    
    inlines = [
        EntryTranslationInline,
    ]    
    
    def get_urls(self):
        from django.conf.urls import patterns, url, include

        def wrap(view):
            def wrapper(*args, **kwargs):
                return self.admin_site.admin_view(view)(*args, **kwargs)
            return update_wrapper(wrapper, view)

        info = self.model._meta.app_label, self.model.__name__.lower()
        info2 = self._translation_model._meta.app_label, self._translation_model.__name__.lower()

        urlpatterns = patterns('',
            url(r'^$', wrap(self._translation_admin.changelist_view), name='%s_%s_changelist' % info),
            url(r'^subadmin/', include(self._translation_admin.urls)),
        )
        return urlpatterns + super(EntryAdmin, self).get_urls() + patterns('',
            url(r'^add/$', wrap(self.add_view), name='%s_%s_add' % info2),
        )

    def urls(self):
        return self.get_urls()
    urls = property(urls)
    
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
'''
admin.site.register(Entry, EntryAdmin)

