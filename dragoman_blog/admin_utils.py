from django.utils.translation import ugettext as _
from django.utils.translation import get_language
from django.contrib import admin
from django.utils.encoding import force_unicode
from django.utils.html import escape
from django.http import Http404, HttpResponseRedirect
from django.core.urlresolvers import reverse
from functools import update_wrapper
from django.contrib.admin.util import unquote
from django.conf import settings

from django import forms
from django.forms.models import BaseInlineFormSet

class GetLanguageMixin(object):
    
    def get_language_request(self, request, as_dict=False, as_qs=False, suffix='', add_suffix=False):
        language_code = request.REQUEST.get(self.language_field, request.REQUEST.get(self.language_field + suffix, get_language()))
        if as_dict:
            return {'translation_language_code': language_code, 'translation_language_field': self.language_field,}
        if as_qs:
            return self.language_field + (add_suffix and suffix or '') +'='+language_code
        return language_code
        
    def get_language_request_tabs(self, request, obj=None):
        tabs = {}
        language_dict = self.get_language_request(request, as_dict=True)
        language_code = language_dict['translation_language_code']
        for code, name in settings.LANGUAGES:
            tabs[code] = {'name': name}
            if code == language_code:
                tabs[code]['current'] = True
        allow_deletion = False
        if obj:
            translations = getattr(obj, self.translation_accessor).values('id', self.language_field)
            if len(translations) > 1:
                allow_deletion = True
            for translation in translations:
                code = translation[self.language_field]
                if code in tabs:
                    tabs[code]['id'] = translation['id']
        return dict(allow_deletion = allow_deletion, language_tabs = tabs, **language_dict)

class AtLeastOneRequiredInlineFormSet(BaseInlineFormSet):

    def clean(self):
        """Check that at least one inline has been filled."""
        super(AtLeastOneRequiredInlineFormSet, self).clean()
        if any(self.errors):
            return
        if not any(cleaned_data and not cleaned_data.get('DELETE', False)
            for cleaned_data in self.cleaned_data):
            raise forms.ValidationError('Translation required, fill in fields or switch language.')
                            
def make_translation_admin(translationmodel,
    SharedAdminBase=admin.ModelAdmin,
    TranslationAdminBase=admin.ModelAdmin,
    TranslationInlineBase=admin.StackedInline,
    return_parts=False):
            
    class BaseTranslationInline(GetLanguageMixin, TranslationInlineBase):
        language_field = 'language_code'
        exclude = ('language_code',)
        
        def queryset(self, request):
            queryset = super(BaseTranslationInline, self).queryset(request)
            queryset = queryset.filter(**{self.language_field:self.get_language_request(request)})
            return queryset
                         
    class TranslationInline(BaseTranslationInline):
        max_num = 1
        model = translationmodel
        template = 'admin/dragoman_blog/stacked_inline.html'
        formset = AtLeastOneRequiredInlineFormSet
                    
    class TranslationAdmin(GetLanguageMixin, TranslationAdminBase):
        language_field = 'language_code'

        list_filter = ('language_code',)
        delete_confirmation_template = 'admin/dragoman_blog/delete_confirmation.html'
        change_list_template = 'admin/dragoman_blog/change_list.html'
        list_display = ('title', 'language_code')

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
            extra_context.update(self.get_language_request(request, as_dict=True, suffix='__exact'))
            return super(TranslationAdmin, self).changelist_view(request, extra_context=extra_context)
                    
        def delete_view(self, request, object_id, extra_context={}):
            extra_context.update(self.get_language_request(request, as_dict=True))      
            resp =  super(TranslationAdmin, self).delete_view(request, object_id, extra_context=extra_context)
            if 'Location' in resp:
                resp['Location'] = resp['Location']+'?'+self.get_language_request(request, as_qs=True)
            return resp

    class SharedAdmin(GetLanguageMixin, SharedAdminBase):
        language_field = 'language_code'

        change_form_template = 'admin/dragoman_blog/change_form.html'
        delete_confirmation_template = 'admin/dragoman_blog/delete_confirmation.html'
        
        translation_model_map = {}
        
        def __init__(self, model, admin_site):
            super(SharedAdmin, self).__init__(model, admin_site)
            self.translation_admin = self.translation[1](self.translation[0], admin_site)
            self.inlines.insert(0, self.translation[2])
            self.translation_model = self.translation[0]
    
            for inline in self.inlines:
                if issubclass(inline, BaseTranslationInline):
                    self.translation_model_map[inline.model] = inline.language_field
    
            for related_object in self.model._meta.get_all_related_objects():
                if related_object.model == self.translation_model:
                    self.translation_accessor = related_object.get_accessor_name()
                        
        translation = (translationmodel, TranslationAdmin, TranslationInline)
        
        def get_object(self, request, object_id):
            obj = super(SharedAdmin, self).get_object(request, object_id)
            if obj:
                try:
                    obj.title = unicode(getattr(obj, self.translation_accessor).get(**{self.language_field:self.get_language_request(request)}))
                except self.translation_model.DoesNotExist:
                    pass
            return obj
            
        def delete_view(self, request, object_id, extra_context={}):
            extra_context.update(self.get_language_request(request, as_dict=True))
            resp =  super(SharedAdmin, self).delete_view(request, object_id, extra_context=extra_context)
            if 'Location' in resp:
                resp['Location'] = resp['Location']+'?'+self.get_language_request(request, as_qs=True)
            return resp
                                 
        def add_view(self, request, form_url='', extra_context={}):
            if request.method != 'POST' and not 'language_code' in request.GET:
                return HttpResponseRedirect(request.path+'?'+self.get_language_request(request, as_qs=True))
            else:
                extra_context.update(self.get_language_request_tabs(request))
                return super(SharedAdmin, self).add_view(request, form_url=form_url, extra_context=extra_context)
                
        def change_view(self, request, object_id, form_url='', extra_context={}):
            if request.method != 'POST' and not 'language_code' in request.GET:
                return HttpResponseRedirect(request.path+'?'+self.get_language_request(request, as_qs=True))
            else:
                obj = self.get_object(request, unquote(object_id))
                extra_context.update(self.get_language_request_tabs(request, obj))
                return super(SharedAdmin, self).change_view(request, object_id, form_url=form_url, extra_context=extra_context)
                
        def response_change(self, request, obj):
            add_suffix = False
            if not ("_continue" in request.POST or "_addanother" in request.POST):
                add_suffix = True 
            resp = super(SharedAdmin, self).response_change(request, obj)
            resp['Location'] = resp['Location']+'?'+self.get_language_request(request, as_qs=True, suffix='__exact', add_suffix=add_suffix)
            return resp
            
        def response_add(self, request, obj):
            add_suffix = False
            if not ("_continue" in request.POST or "_addanother" in request.POST):
                add_suffix = True
            resp = super(SharedAdmin, self).response_add(request, obj)
            resp['Location'] = resp['Location']+'?'+self.get_language_request(request, as_qs=True, suffix='__exact', add_suffix=add_suffix)
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
                url(r'^translation/', include(self.translation_admin.urls)),
                url(r'^$', wrap(self.translation_admin.changelist_view), name='%s_%s_changelist' % info2),
            )
            return urlpatterns + super(SharedAdmin, self).get_urls() + patterns('',
                url(r'^add/$', wrap(self.add_view), name='%s_%s_add' % info2),
            )
    
        def urls(self):
            return self.get_urls()
        urls = property(urls)
        
        def save_formset(self, request, form, formset, change):
            if formset.model in self.translation_model_map:
                formset.save(commit=False)
                for f in formset.forms:
                    if f.is_valid():
                        obj = f.instance 
                        setattr(obj, self.translation_model_map[formset.model], self.get_language_request(request))
            super(SharedAdmin, self).save_formset(request, form, formset, change)
            
    if return_parts:
        return SharedAdmin, TranslationAdmin, BaseTranslationInline, TranslationInline    
    return SharedAdmin
