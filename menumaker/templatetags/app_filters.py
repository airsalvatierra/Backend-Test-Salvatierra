from django import template

from comun.utils import check_if_is_supervisor

register = template.Library()


# show/hide menus if is supervisor(nora)
@register.simple_tag(takes_context=True)
def show_supervisor_menus(context):
    return check_if_is_supervisor(context['request'].user.username)
