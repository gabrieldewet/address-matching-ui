from django import template

register = template.Library()


@register.filter
def multiply(value, arg):
    """Multiply the value by the argument"""
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return 0


@register.filter
def levenshtein_ratio(value, arg):
    """Calculate the Levenshtein ratio between two strings"""
    return 0, []
