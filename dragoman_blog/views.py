from dragoman_blog.models import EntryTranslation
from django.views.generic.list import ListView
from django.utils.translation import get_language


class ListByTagView(ListView):

    """ View for listing posts by tags"""
    template_name = "dragoman_blog/entrytranslation_list_by_tag.html"
    model = EntryTranslation

    def get_queryset(self):
        try:
            tag = self.kwargs['tag']
        except:
            tag = ''
        if (tag != ''):
            object_list = self.model.objects.filter(
                tags__name=tag, language_code=get_language(), is_published=True)
        else:
            object_list = self.model.objects.none()
        return object_list

    def get_context_data(self, **kwargs):
        context = super(ListByTagView, self).get_context_data(**kwargs)
        context['tag'] = self.kwargs['tag']
        return context
