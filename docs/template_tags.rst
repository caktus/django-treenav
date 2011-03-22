Builtin Template Tags
=====================

Generally you will get access to the menus created by treenav through 
template tags.  Currently treenav offers four template tags to use.

Show Treenav
------------
.. highlight:: html+django
::

    {% show_treenav "top-level-slug" %}


This is the canonical tag you will be using.  It outputs treeing list starting
with all the children of menu item which has a slug matching top-level-slug.
This will make sure that the page being rendered and its parent MenuItems have
the html class active on them.


Single Level Menu
-----------------

::

    {% single_level_menu "top-level-slug" 6 %}    

This is used to build single level navigations.  The first argument is used to 
define the MenuItem that will be used as the top of the tree and the second argument
defines the level to be displayed.  Often this will be used when a page has multiple
menus where one menu is the top level, and another is the first level
of the active page.

Render Menu Children
--------------------

::
    
    {% render_menu_children "parent-slug" %}

This renders as a treeing list all the descendents of the MenuItem with the first
argument as its slug.

Show Menu Crumbs
----------------

::
    
    {% show_menu_crumbs "bottom-level-slug" %}


Builds a list of the active MenuItems above the "bottom-level-slug" to build
a breadcrumb stucture so that all of the items between the top level item
and the selected item are shown.
