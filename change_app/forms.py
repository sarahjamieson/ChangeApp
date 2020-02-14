from django import forms

from db.models import Change
from db.models import ChangeSuggestion
from db.models import Hub
from web.forms import SemanticMCF


class ChangeSuggestionForm(forms.ModelForm):
    title = forms.CharField(
        max_length=80,
        required=True,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Title of the suggested change'
            }
        )
    )
    change_type = forms.ChoiceField(
        choices=ChangeSuggestion.ChangeTypes.choices,
        widget=forms.Select(
            attrs={
                'class': 'ui dropdown'
            }
        )
    )
    hub = forms.ModelChoiceField(
        queryset=Hub.objects.all(),
        widget=forms.Select(
            attrs={
                'class': 'ui dropdown'
            }
        )
    )
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

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(ChangeSuggestionForm, self).__init__(*args, **kwargs)
        if user:
            user_hubs = user.hubs.all()
            self.fields['hub'].queryset = user_hubs
        change_type_choices = self.fields['change_type'].choices
        self.fields['change_type'].choices = [('', 'Type of change')] + [
            change_type for change_type in change_type_choices
        ]


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
