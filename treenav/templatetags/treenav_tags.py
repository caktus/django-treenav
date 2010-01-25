import copy

from django import template
from django.template.loader import render_to_string

from treenav.templatetags import CaktNode, parse_args_kwargs
from treenav.models import MenuItem


register = template.Library()


def copy_context(orig):
    new = {}
    for key in ['PATH_INFO']:
        new['request'][key] = orig['request'][key]
    return new


class SingleLevelMenuNode(CaktNode):
    """
    Renders the nth-level items of a named Menu model object.
    """
    
    def render_with_args(self, context, slug, level):
        level = int(level)
        try:
            menu = MenuItem.objects.get(slug=slug)
        except MenuItem.DoesNotExist:
            return ''
        root = menu.to_tree()
        active_leaf = root.set_active(context['request'].META['PATH_INFO'])
        children_context = copy.copy(context)
        if active_leaf:
            context['active_menu_items'] = active_leaf.get_active_items()
            if len(context['active_menu_items']) <= level:
                return ''
            children_context['menuitem'] = context['active_menu_items'][level]
        elif level == 0:
            children_context['menuitem'] = root
        else:
            return ''
        children_context['full_tree'] = False
        children_context['single_level'] = True
        return render_to_string('treenav/menuitem.html', children_context)


# Usage example:
# {% single_level_menu "main" 6 %}
@register.tag
def single_level_menu(parser, token):
    tag_name, args, kwargs = parse_args_kwargs(parser, token)
    return SingleLevelMenuNode(*args, **kwargs)


class MenuNode(CaktNode):
    """
    Renders the top-level items of a named Menu model object.
    """
    
    def render_with_args(self, context, slug, full_tree=False):
        try:
            menu = MenuItem.objects.get(slug=slug)
        except MenuItem.DoesNotExist:
            return ''
        root = menu.to_tree()
        active_leaf = root.set_active(context['request'].META['PATH_INFO'])
        if active_leaf:
            context['active_menu_items'] = active_leaf.get_active_items()
        children_context = copy.copy(context)
        children_context['menuitem'] = root
        children_context['full_tree'] = ('True' == full_tree)
        return render_to_string('treenav/menuitem.html', children_context)

# Usage example:
# {% menu "main" %}
    
@register.tag(name='show_treenav')
def show_treenav(parser, token):
    tag_name, args, kwargs = parse_args_kwargs(parser, token)
    return MenuNode(*args, **kwargs)


class RenderMenuChildrenNode(template.Node):
    """
    Renders the children of the given MenuItem model object.
    """
    def __init__(self, item):
        self.item = template.Variable(item)
        
    def render(self, context):
        item = self.item.resolve(context)
        children_context = copy.copy(context)
        children_context['menuitem'] = item
        return render_to_string('treenav/menuitem.html', children_context)

# Usage example:
# {% menu_item_status item %}

@register.tag(name='render_menu_children')
def do_render_menu_children(parser, token):
    menu_path = token.split_contents()
    return RenderMenuChildrenNode(menu_path[1])
