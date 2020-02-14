from django import forms

from db.models import Change
from db.models import ChangeSuggestion
from web.forms import SemanticMCF


class ChangeSuggestionForm(forms.ModelForm):
    updates = forms.ModelChoiceField(
        queryset=Change.objects.all()
    )
    contributes_to = forms.ModelChoiceField(
        queryset=Change.objects.all()
    )
    includes = SemanticMCF(
        queryset=Change.objects.all(),
        empty_label='Subchanges comprising this change'
    )
    class Meta:
        model = ChangeSuggestion
        fields = (
            'title',
            'change_type',
            'hub',
            'summary',
            'impact',
            'strategy',
        )
