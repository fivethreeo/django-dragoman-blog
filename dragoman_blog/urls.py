from django.conf.urls import url, patterns

# from hvad_blog.feeds import EntriesFeed, TaggedEntriesFeed, AuthorEntriesFeed
from dragoman_blog.models import Entry, EntryTranslation

from django.utils.translation import get_language
from django.views.generic.dates import DateDetailView, ArchiveIndexView, YearArchiveView, MonthArchiveView, DayArchiveView
from dragoman_blog.views import ListByTagView


class EntryDateDetail(DateDetailView):

    def get_queryset(self):
        return super(EntryDateDetail, self).get_queryset().filter(language_code=get_language())


class EntryArchiveIndex(ArchiveIndexView):

    def get_queryset(self):
        return super(EntryArchiveIndex, self).get_queryset().filter(language_code=get_language())


class EntryYearArchive(YearArchiveView):

    def get_queryset(self):
        return super(EntryYearArchive, self).get_queryset().filter(language_code=get_language())


class EntryMonthArchive(MonthArchiveView):

    def get_queryset(self):
        return super(EntryMonthArchive, self).get_queryset().filter(language_code=get_language())


class EntryDayArchive(DayArchiveView):

    def get_queryset(self):
        return super(EntryDayArchive, self).get_queryset().filter(language_code=get_language())


blog_info_dict = {
    'queryset': EntryTranslation.objects.all(),
    'date_field': 'pub_date',
    'allow_empty': True,
    'paginate_by': 15,
}

blog_detail = EntryDateDetail.as_view(
    queryset=EntryTranslation.objects.all(),
    date_field='pub_date',
    month_format='%m',
    slug_field='slug',
)

urlpatterns = patterns('',
    url(r'^$', EntryArchiveIndex.as_view(**blog_info_dict),
       name='dragoman_blog_archive_index'),

    url(r'^(?P<year>\d{4})/$', EntryYearArchive.as_view(**blog_info_dict),
        name='dragoman_blog_archive_year'),

    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/$',
       EntryMonthArchive.as_view(month_format='%m', **blog_info_dict),
       name='dragoman_blog_archive_month'),

    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/$',
       EntryDayArchive.as_view(month_format='%m', **blog_info_dict),
       name='dragoman_blog_archive_day'),

    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<slug>[-\w]+)/$',
       blog_detail, name='dragoman_blog_detail'),

    url(r"^tag/(?P<tag>.*)/$", ListByTagView.as_view(),
       name="dragoman_blog_list_by_tag"),
)
