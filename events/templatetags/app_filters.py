from django import template

register = template.Library()

@register.filter("made_events")
def made_events(args):
    user, event = args.split(',')
    if event==user:  #event is a string,, event.author=user
        return event
    


@register.filter("invited_events")
def invited_events(user,invitees):
    if invitees == user:
        return event.name


