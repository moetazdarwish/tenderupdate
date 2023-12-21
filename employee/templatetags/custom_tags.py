from django import template
register = template.Library()

@register.filter(name="group")
def group(u, group_names):
    group_names = group_names.split(',')
    return u.groups.filter(name__in=group_names).exists()
@register.filter
def duration(td):
    if td is None:
        return '{} hours {} min'.format(00, 00)
    total_seconds = int(td.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60

    return '{} hours {} min'.format(hours, minutes)