from __future__ import unicode_literals

from django import VERSION

import datetime


from django.utils.translation import ugettext as _
from django.utils.translation import get_language
from django.utils import timezone
from django.utils import six

from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.conf import settings

from taggit.managers import TaggableManager

from dragoman_blog.utils.model_loading import get_dragoman_model_string

try:
    from django.utils import timezone
except ImportError:
    timezone = None
    
class BaseEntry(models.Model):
    
    class Meta:
        verbose_name = _('Entry')
        verbose_name_plural = _('Entrys')
        abstract = True
            
    def __unicode__(self):
        return getattr(self, 'title', 'Untranslated')
    
class BaseEntryTranslation(models.Model):
    
    class Meta:
        verbose_name = _('Entry')
        verbose_name_plural = _('Entrys')
        abstract = True
    
    language_code = models.CharField(_('language'), max_length=15, db_index=True, choices=settings.LANGUAGES)
    
    master = models.ForeignKey(get_dragoman_model_string('Entry'))
    is_published = models.BooleanField(_('is published'))
    pub_date = models.DateTimeField(_('publish at'), default=timezone.now)
     
    title = models.CharField(_('title'), max_length=255)
    slug = models.SlugField(_('slug'), max_length=255)
    author = models.ForeignKey('auth.User', null=True, blank=True, verbose_name=_("author"))
    
    tags = TaggableManager(through='dragoman_blog.TranslationTagged')
    
    def __unicode__(self):
        return self.title
    
    def _get_absolute_url(self):
        pub_date = self.pub_date
        slug = self.slug

        local_pub_date = timezone.localtime(pub_date)
    
        return ('dragoman_blog_detail', (), {
            'year': local_pub_date.year,
            'month': local_pub_date.strftime('%m'),
            'day': local_pub_date.strftime('%d'),
            'slug': slug
        })
    get_absolute_url = models.permalink(_get_absolute_url)
    