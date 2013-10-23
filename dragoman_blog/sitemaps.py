from django.contrib.sitemaps import Sitemap
from hvad_blog.models import Entry

class BlogSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.5

    def items(self):
        return Entry.objects.filter(entry__entrytranslation__is_published=True)

    def lastmod(self, obj):
        return obj.pub_date