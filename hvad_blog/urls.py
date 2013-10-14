from django.conf.urls import url, patterns

from django.views.generic.dates import DateDetailView, ArchiveIndexView, YearArchiveView, MonthArchiveView, DayArchiveView
# from hvad_blog.feeds import EntriesFeed, TaggedEntriesFeed, AuthorEntriesFeed

from hvad_blog.models import Entry

blog_info_dict = {
    'queryset': Entry.translations.related.model.objects.all(),
    'date_field': 'pub_date',
    'allow_empty': True,
    'paginate_by': 15,
}

blog_detail = DateDetailView.as_view(
    queryset=Entry.translations.related.model.objects.all(),
    date_field='pub_date',
    month_format='%m',
    slug_field='slug',
)

urlpatterns = patterns('',
    url(r'^$', ArchiveIndexView.as_view(**blog_info_dict), name='hvad_blog_archive_index'),
    
    url(r'^(?P<year>\d{4})/$', YearArchiveView.as_view(**blog_info_dict), name='hvad_blog_archive_year'),
    
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/$',
        MonthArchiveView.as_view(month_format='%m', **blog_info_dict), name='hvad_blog_archive_month'),
    
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/$',
        DayArchiveView.as_view(month_format='%m', **blog_info_dict), name='hvad_blog_archive_day'),
    
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<slug>[-\w]+)/$',
        blog_detail, name='hvad_blog_detail')
)