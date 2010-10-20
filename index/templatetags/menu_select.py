from django import template

register = template.Library()

@register.filter
# truncate after a certain number of characters
def section(value, arg):
    if value.split("/")[1] == arg:
        return "class=current"
    else:
        return ""
