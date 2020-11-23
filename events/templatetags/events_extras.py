from django import template

register = template.Library()

@register.filter(name='is_marked')
def is_marked(value, arg):
    """Checks if user is marked, for use in attendees and bookmarkers"""
    already_marked = False

    for user in value.all() :
        if (arg == user) :
            already_marked = True

    return already_marked
