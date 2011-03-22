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
with all the children of menu item which has a slug matching top-level-slug.  To
see the HTML output go to `Menu HTML Example`_.

Render Menu Children
--------------------

::
    
    {% render_menu_children "parent-slug" %}

This renders as a treeing list all the descendents of the MenuItem with the first
argument as its slug.


Menu HTML Example
-----------------

The above two templates tags use the same template to generate lists although
single_level_menu will not include the nested URLS.

Note that Tests is the page currently active, it as well as its parents have 
the class "active-menu-item" attached to them.  The links on active nodes are 
marked with the class "active-menu-item-link".  The depth-N class, where N starts 
at 0 and increases for each nested UL, it is often used to help apply custom CSS 
depending on how deeply a UL is nested.


.. highlight:: html

::

    <ul id="menu-primary-nav" class="menu depth-0">   
        <li id="menu-item-home" class="inactive-menu-item top-level">
            <a class="inactive-menu-item-link top-level-link" href="/" title="Home">Home</a>    
        </li>
        <li id="menu-item-about" class="active-menu-item top-level">
            <a class="active-menu-item-link top-level-link" href="/about/" title="About">About</a>
            <ul id="menu-home" class="menu depth-1">
                <li id="menu-item-tests" class="active-menu-item about-child">
                    <a class="active-menu-item-link about-sub-child-link" href="/tests/" title="Tests">Tests</a>
                </li>
            </ul>
        </li>
    </ul>


Single Level Menu
-----------------

::

    {% single_level_menu "top-level-slug" 6 %}    

This is used to build single level navigations.  The first argument is used to 
define the MenuItem that will be used as the top of the tree and the second argument
defines the level to be displayed.  Often this will be used when a page has multiple
menus where one menu is the top level, and another is the first level
of the active page.

For HTML output go to `Menu HTML Example`_.  Although the
example is two levels, this can only output one.  One thing to note is the if you
select a depth of 3 then the depth class mentioned above will be depth-3, not 0
even though its the top(and only) UL.

Show Menu Crumbs
----------------

::
    
    {% show_menu_crumbs "bottom-level-slug" %}


Builds a list of the active MenuItems above the "bottom-level-slug" to build
a breadcrumb stucture so that all of the items between the top level item
and the selected item are shown.
