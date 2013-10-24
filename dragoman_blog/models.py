from __future__ import unicode_literals

from django.utils.translation import get_language

from django.db import models
from django.contrib.contenttypes.models import ContentType

from taggit.models import GenericTaggedItemBase

from dragoman_blog.utils.model_loading import load_class

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

ENTRY_MODEL = getattr(settings, 'DRAGOMAN_BLOG_ENTRY_MODEL',
                         'dragoman_blog.model_defaults.Entry')
Entry = load_class(ENTRY_MODEL, 'DRAGOMAN_BLOG_ENTRY_MODEL')

ENTRYTRANSLATION_MODEL = getattr(settings, 'DRAGOMAN_BLOG_ENTRYTRANSLATION_MODEL',
                         'dragoman_blog.model_defaults.EntryTranslation')
EntryTranslation = load_class(ENTRYTRANSLATION_MODEL, 'DRAGOMAN_BLOG_ENTRYTRANSLATION_MODEL')