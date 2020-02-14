from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import FormView
from django.views.generic.detail import SingleObjectMixin


from db.models import Change
from db.models import Suggestion


class SuggestView(LoginRequiredMixin, SingleObjectMixin, FormView):
    model = Suggestion
    context_object_name = 'suggestion'
    form_class = For
    template_name = 'change_app/suggestion.html'
