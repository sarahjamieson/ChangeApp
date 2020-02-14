from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import FormView
from django.views.generic.detail import SingleObjectMixin


from change_app.forms import ChangeSuggestionForm
from db.models import Change
from db.models import ChangeSuggestion


class SuggestView(LoginRequiredMixin, FormView):
    model = ChangeSuggestion
    context_object_name = 'suggestion'
    form_class = ChangeSuggestionForm
    template_name = 'change_app/suggestion.html'
