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
    def __init__(self, *args, **kwargs):
        super(SingleLevelMenuNode, self).__init__(*args, **kwargs)
    
    def __repr__(self):
        return "<SingleLevelMenuNode>"
    
    def render_with_args(self, context, menu_name, level, suggestion=None):
        menu = Menu.objects.get(name=menu_name)
        children_context = copy_context(context)
        children_context['menu_depth'] = level
        children_context['skip_children'] = True
        
        if suggestion:
            try:
                node = MenuItem.objects.get(
                    menu=menu,
                    id=suggestion,
                )
            except MenuItem.DoesNotExist:
                node = None
        else:
            try:
                node = MenuItem.objects.get(
                    menu=menu,
                    href=context['request'].META['PATH_INFO'],
                )
            except MenuItem.DoesNotExist:
                node = None
        
        if node:
            if level > (node.height() + 1) or level <= 0:
                raise AttributeError('Invalid menu level %s' % level)
            
            # step up tree until we find wanted node height
            while node.height() >= level:
                node = node.up()
        
            children_context['menu_slug'] = node.slug
            children_context['menu_items'] = node.get_children()
        
        return render_to_string('cms/menu.html', children_context)


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
            context['active_menu_items'] = active_leaf.get_ancestors()
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
