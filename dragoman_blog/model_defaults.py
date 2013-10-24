from django.utils.translation import ugettext as _
from dragoman_blog.model_bases import BaseEntry, BaseEntryTranslation

class Entry(BaseEntry):
    
    class Meta:
        verbose_name = _('Entry')
        verbose_name_plural = _('Entrys')
        abstract = False
        app_label = 'dragoman_blog'
    
class EntryTranslation(BaseEntryTranslation):
    
    class Meta:
        verbose_name = _('Entry')
        verbose_name_plural = _('Entrys')
        abstract = False
        app_label = 'dragoman_blog'