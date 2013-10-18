from django.utils.translation import get_language
from django.contrib import admin
from hvad_blog.models import Entry, EntryTranslation
from django.utils.encoding import force_unicode
from django.utils.html import escape
from django.http import Http404, HttpResponseRedirect
from django.core.urlresolvers import reverse
from functools import update_wrapper
from django.contrib.admin.util import unquote
from django.conf import settings

class GetLanguageMixin(object):
    
    def get_language(self, request, as_dict=False, as_qs=False, suffix=''):
        language_code = request.REQUEST.get('language_code', request.REQUEST.get('language_code'+ suffix, get_language()))
        if as_dict:
            return {'language_code': language_code}
        if as_qs:
            return 'language_code' + suffix +'='+language_code
        return language_code    
        
    def get_language_tabs(self, request, obj=None):
        tabs = {}
        for code, name in settings.LANGUAGES:
            tabs[code] = {'name': name}
        allow_deletion = False
        if obj:
            translations = self.translation_model.objects.filter(master=obj).values('id', 'language_code')
            if len(translations) > 1:
                allow_deletion = True
            for translation in translations:
                code = translation['language_code']
                if code in tabs:
                    tabs[code]['id'] = translation['id']
        return {'allow_deletion': allow_deletion, 'language_tabs': tabs, 'language_tabs_code': self.get_language(request)}
                    
def make_translation_admin(translationmodel,
    SharedAdminBase=admin.ModelAdmin,
    TranslationAdminBase=admin.ModelAdmin,
    TranslationInlineBase=admin.StackedInline,
    return_parts=False):
    
    class TranslationAdmin(GetLanguageMixin, TranslationAdminBase):
        
        list_filter = ('language_code',)
        delete_confirmation_template = 'admin/hvad_blog/delete_confirmation.html'
        change_list_template = 'admin/hvad_blog/change_list.html'

        def change_view(self, request, object_id, form_url='', extra_context=None):
            "The 'change' admin view for this model."
            model = self.model
            opts = model._meta
    
            obj = self.get_object(request, unquote(object_id))
    
            if not self.has_change_permission(request, obj):
                raise PermissionDenied
    
            if obj is None:
                raise Http404(_('%(name)s object with primary key %(key)r does not exist.') % {'name': force_unicode(opts.verbose_name), 'key': escape(object_id)})
            return HttpResponseRedirect(reverse('admin:hvad_blog_entry_change', args=[obj.master.pk])+'?language_code='+obj.language_code)
    
        def changelist_view(self, request, extra_context={}):
            extra_context.update(self.get_language(request, as_dict=True, suffix='__exact'))
            return super(TranslationAdmin, self).changelist_view(request, extra_context=extra_context)
                    
        def delete_view(self, request, object_id, extra_context={}):
            extra_context.update(self.get_language(request, as_dict=True))      
            resp =  super(TranslationAdmin, self).delete_view(request, object_id, extra_context=extra_context)
            if 'Location' in resp:
                resp['Location'] = resp['Location']+'?'+self.get_language(request, as_qs=True)
            return resp
            
    class BaseTranslationInline(GetLanguageMixin, TranslationInlineBase):
        exclude = ('language_code',)
        
        def queryset(self, request):
            queryset = super(BaseTranslationInline, self).queryset(request)
            queryset = queryset.filter(language_code=self.get_language(request))
            return queryset
                         
    class TranslationInline(BaseTranslationInline):
        max_num = 1
        model = translationmodel
        template = 'admin/hvad_blog/stacked_inline.html'
                
    class SharedAdmin(GetLanguageMixin, SharedAdminBase):

        change_form_template = 'admin/hvad_blog/change_form.html'
        delete_confirmation_template = 'admin/hvad_blog/delete_confirmation.html'
        
        def __init__(self, model, admin_site):
            super(SharedAdmin, self).__init__(model, admin_site)
            self.translation_admin = self.translation[1](self.translation[0], admin_site)
            self.inlines.insert(0, self.translation[2])
            self.translation_model = self.translation[0]
                        
        translation = (translationmodel, TranslationAdmin, TranslationInline)

        def delete_view(self, request, object_id, extra_context={}):
            extra_context.update(self.get_language(request, as_dict=True))
            resp =  super(SharedAdmin, self).delete_view(request, object_id, extra_context=extra_context)
            if 'Location' in resp:
                resp['Location'] = resp['Location']+'?'+self.get_language(request, as_qs=True)
            return resp
                                 
        def add_view(self, request, form_url='', extra_context={}):
            if not 'language_code' in request.GET:
                return HttpResponseRedirect(request.path+'?'+self.get_language(request, as_qs=True))
            else:
                extra_context.update(self.get_language_tabs(request))
                return super(SharedAdmin, self).add_view(request, form_url=form_url, extra_context=extra_context)
                
        def change_view(self, request, object_id, form_url='', extra_context={}):
            if not 'language_code' in request.GET:
                return HttpResponseRedirect(request.path+'?'+self.get_language(request, as_qs=True))
            else:
                obj = self.get_object(request, unquote(object_id))
                extra_context.update(self.get_language_tabs(request, obj))
                return super(SharedAdmin, self).change_view(request, object_id, form_url=form_url, extra_context=extra_context)
            
        def response_change(self, request, obj):
            resp = super(SharedAdmin, self).response_change(request, obj)
            resp['Location'] = resp['Location']+'?'+self.get_language(request, as_qs=True, suffix='__exact')
            return resp
            
        def response_add(self, request, obj):
            resp = super(SharedAdmin, self).response_add(request, obj)
            resp['Location'] = resp['Location']+'?'+self.get_language(request, as_qs=True, suffix='__exact')
            return resp
            
        def get_urls(self):
            from django.conf.urls import patterns, url, include
    
            def wrap(view):
                def wrapper(*args, **kwargs):
                    return self.admin_site.admin_view(view)(*args, **kwargs)
                return update_wrapper(wrapper, view)
    
            info = self.model._meta.app_label, self.model.__name__.lower()
            info2 = self.translation_model._meta.app_label, self.translation_model.__name__.lower()
    
            urlpatterns = patterns('',
                url(r'^$', wrap(self.translation_admin.changelist_view), name='%s_%s_changelist' % info),
                url(r'^subadmin/', include(self.translation_admin.urls)),
                url(r'^$', wrap(self.translation_admin.changelist_view), name='%s_%s_changelist' % info2),
            )
            return urlpatterns + super(SharedAdmin, self).get_urls() + patterns('',
                url(r'^add/$', wrap(self.add_view), name='%s_%s_add' % info2),
            )
    
        def urls(self):
            return self.get_urls()
        urls = property(urls)
        
        def save_formset(self, request, form, formset, change):
            if formset.model ==  self.translation_model:
                formset.save(commit=False)
                for f in formset.forms:
                    obj = f.instance 
                    obj.language_code = self.get_language(request)
                    obj.save()
                formset.save_m2m()
            else:
                super(SharedAdmin, self).save_formset(request, form, formset, change)
    if return_parts:
        return SharedAdmin, TranslationAdmin, BaseTranslationInline, TranslationInline    
    return SharedAdmin
    
admin.site.register(Entry, make_translation_admin(EntryTranslation))

                
