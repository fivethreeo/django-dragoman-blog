from django.utils.translation import ugettext as _
from dragoman_blog.model_bases import BaseEntry, BaseEntryTranslation

class Entry(BaseEntry):
    
    placeholder = PlaceholderField('dragoman_placeholder')

    class Meta:
        verbose_name = _('Entry')
        verbose_name_plural = _('Entrys')
        abstract = False
        app_label = 'dragoman_blog'