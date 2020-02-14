from django.forms import ModelMultipleChoiceField


class SemanticMCF(ModelMultipleChoiceField):
    """Class to allow for multiple choice dropdowns to render correctly.

    In Semantic UI, multiple dropwdown <select> object get their placeholder
    value from an included option with value="" ie <select><option value=""> ..
    However the Django default ModelMultipleChoiceField does not allow for
    creation of this as with other Fields as the inherited value empty_label is
    set to None. By overriding this value after the __init__ call we can use
    the django form to full potential to render form without need for extensive
    JS.
    """
    def __init__(self, queryset, empty_label, **kwargs):
        super(SemanticMCF, self).__init__(queryset, **kwargs)
        self.empty_label = empty_label



