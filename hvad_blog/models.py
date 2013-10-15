from __future__ import unicode_literals

from django import VERSION

import datetime

from django.utils.translation import ugettext as _
from django.utils.translation import get_language
from django.utils import timezone
from django.utils import six

from django.db import models
from hvad.models import TranslatableModel, TranslatedFields, create_translations_model

from taggit.managers import TaggableManager
from taggit.models import GenericTaggedItemBase

try:
    from django.utils import timezone
except ImportError:
    timezone = None
    
class TranslationTagged(GenericTaggedItemBase):
    
    tag = models.ForeignKey('taggit.Tag', related_name="%(app_label)s_%(class)s_items")
    language_code = models.CharField(max_length=15, db_index=True)
    
    @classmethod
    def lookup_kwargs(cls, instance):
        return dict(language_code=instance.language_code, **GenericTaggedItemBase.lookup_kwargs(instance))

    @classmethod
    def bulk_lookup_kwargs(cls, instances):
        if isinstance(instances, QuerySet):
            return dict(language_code=instances._language_code, **GenericTaggedItemBase.bulk_lookup_kwargs(instances))
        else:
            return dict(language_code=instances[0].language_code, **GenericTaggedItemBase.bulk_lookup_kwargs(instances))

    @classmethod
    def tags_for(cls, model, instance=None):
        ct = ContentType.objects.get_for_model(model)
        kwargs = {
            "%s__content_type" % cls.tag_relname(): ct
        }
        if instance is not None:
            kwargs["%s__object_id" % cls.tag_relname()] = instance.pk
            kwargs["%s__language_code" % cls.tag_relname()] = instance.language_code
        else:
            kwargs["%s__language_code" % cls.tag_relname()] = get_language()
        return cls.tag_model().objects.filter(**kwargs).distinct()
        
class Entry(TranslatableModel):

    translations = TranslatedFields(
        is_published = models.BooleanField(_('is published')),
        pub_date = models.DateTimeField(_('publish at'), default=timezone.now),
         
        title = models.CharField(_('title'), max_length=255),
        slug = models.SlugField(_('slug'), max_length=255),
        author = models.ForeignKey('auth.User', null=True, blank=True, verbose_name=_("author")),
        tags = TaggableManager(through=TranslationTagged)
    )

    def _get_absolute_url(self):
        pub_date = self.lazy_translation_getter('pub_date', None)
        slug = self.lazy_translation_getter('slug', None)

        local_pub_date = timezone.localtime(pub_date)
    
        return ('hvad_blog_detail', (), {
            'year': local_pub_date.year,
            'month': local_pub_date.strftime('%m'),
            'day': local_pub_date.strftime('%d'),
            'slug': self.slug
        })
    get_absolute_url = models.permalink(_get_absolute_url)
    
    def __unicode__(self):
        return self.lazy_translation_getter('title', 'No title')
        
class EntryTranslation(models.Model):
    pass
