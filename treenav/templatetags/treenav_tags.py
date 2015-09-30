from django import template
from django.core.cache import cache
from django.template.loader import render_to_string

from treenav.models import MenuItem
from treenav.templatetags import CaktNode, parse_args_kwargs


register = template.Library()


def get_menu_item(slug):
    cache_key = 'menu-%s' % slug
    menu = cache.get(cache_key)
    if not menu:
        try:
            menu = MenuItem.objects.get(slug=slug)
        except MenuItem.DoesNotExist:
            menu = None
        cache.set(cache_key, menu)
    return menu


def new_context(parent_context):
    """ Create new context rather than modifying parent context """
    if 'request' in parent_context:
        return {'request': parent_context['request']}
    else:
        return {}


class SingleLevelMenuNode(CaktNode):
    """
    Renders the nth-level items of a named Menu model object.
    """

    def render_with_args(self, context, slug, level):
        level = int(level)
        menu = get_menu_item(slug)
        if not menu:
            return ''
        parent_context = context
        context = new_context(parent_context)
        root = menu.to_tree()
        if 'request' in context:
            active_leaf = root.set_active(context['request'].META['PATH_INFO'])
        else:
            active_leaf = None
        if active_leaf:
            context['active_menu_items'] = active_leaf.get_active_items()
            if len(context['active_menu_items']) <= level:
                return ''
            context['menuitem'] = context['active_menu_items'][level]
        elif level == 0:
            context['menuitem'] = root
        else:
            return ''
        context['full_tree'] = False
        context['single_level'] = True
        return render_to_string('treenav/menuitem.html', context)


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
        # don't modify the parent context
        parent_context = context
        context = new_context(parent_context)
        menu = get_menu_item(slug)
        if not menu:
            return ''
        root = menu.to_tree()
        if 'request' in context:
            active_leaf = root.set_active(context['request'].META['PATH_INFO'])
        else:
            active_leaf = None
        if active_leaf:
            context['active_menu_items'] = active_leaf.get_active_items()
        context['menuitem'] = root
        context['full_tree'] = ('True' == full_tree)
        return render_to_string('treenav/menuitem.html', context)


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
        parent_context = context
        item = self.item.resolve(parent_context)
        context = new_context(parent_context)
        context['menuitem'] = item
        context['full_tree'] = parent_context['full_tree']
        return render_to_string('treenav/menuitem.html', context)


@register.tag(name='render_menu_children')
def do_render_menu_children(parser, token):
    menu_path = token.split_contents()
    return RenderMenuChildrenNode(menu_path[1])


class ActiveMenuItemsNode(CaktNode):
    def render_with_args(self, context, slug):
        parent_context = context
        context = new_context(parent_context)
        menu = get_menu_item(slug)
        if not menu:
            return ''
        root = menu.to_tree()
        if 'request' in context:
            active_leaf = root.set_active(context['request'].META['PATH_INFO'])
        else:
            active_leaf = None
        if active_leaf:
            context['active_menu_items'] = active_leaf.get_active_items()
        return render_to_string('treenav/menucrumbs.html', context)


@register.tag()
def show_menu_crumbs(parser, token):
    tag_name, args, kwargs = parse_args_kwargs(parser, token)
    return ActiveMenuItemsNode(*args, **kwargs)
