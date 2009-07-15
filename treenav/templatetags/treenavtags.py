import copy

from django import template
from django.template.loader import render_to_string

from caktus.django.templatetags import CaktNode, parse_args_kwargs

from treenav.models import MenuItem

from mptt.utils import previous_current_next

# import treenav
# print treenav

register = template.Library()


# import copy
# 
# 
# from django.conf import settings
# from django.template.loader import render_to_string
# from django.contrib.auth.models import User
# from django.utils.encoding import smart_str
# from django.template import Node, NodeList, Variable, Library
# from django.template import TemplateSyntaxError, VariableDoesNotExist
# from django.core.urlresolvers import reverse

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


class Item(object):
    def __init__(self, node):
        self.parent = None
        self.node = node
        self.children = []
        self.active = False
    
    def __repr__(self):
        return str(self.node)
    
    def add_child(self, item):
        item.parent = self
        self.children.append(item)
    
    def set_active(self, href):
        if self.node.href == href:
            self.active = True
            parent = self.parent
            while parent:
                parent.active = True
                parent = parent.parent
            return self
        else:
            self.active = False
            for child in self.children:
                child.set_active(href)
    
    def to_dict(self):
        return {
            'node': self.node,
            'active': self.active,
            'children': [c.to_dict() for c in self.children],
        }


class MenuNode(CaktNode):
    """
    Renders the top-level items of a named Menu model object.
    """
    
    def render_with_args(self, context, slug, full_tree=False):
        try:
            menu = MenuItem.objects.get(slug=slug)
        except MenuItem.DoesNotExist:
            return ''
        item = root = Item(menu)
        for prev, curr, next in previous_current_next(menu.get_descendants()):
            previous_item = item
            item = Item(curr)
            if not prev or prev.level < curr.level:
                previous_item.add_child(item)
            elif prev and prev.level > curr.level:
                diff = prev.level - curr.level
                parent = previous_item
                while parent.node.level >= curr.level:
                    parent = parent.parent
                parent.add_child(item)
            else:
                previous_item.parent.add_child(item)
        
        root.set_active(context['request'].META['PATH_INFO'])
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
