from django.views.generic import TemplateView


class IndexView(TemplateView):
    """Base page of the app.
    """
    template_name = 'index.html'
