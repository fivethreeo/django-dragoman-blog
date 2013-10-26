from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from django.utils.translation import ugettext_lazy as _

class DragomanBlogApphook(CMSApp):
    name = _("Dragoman Blog Apphook")
    urls = ["dragoman_blog.urls"]

apphook_pool.register(DragomanBlogApphook)