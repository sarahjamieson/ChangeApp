from django import template


register = template.Library()


@register.filter(name='range')
def to_range(value):
    """Returns a list of length <value>
    """
    return range(value)


