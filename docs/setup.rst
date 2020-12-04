Setup
=====

.. highlight:: html+django

#. Login to the admin and build your menu item hierarchy
#. Load the ``treenav_tags`` in your template and render the menu where the
   `show_treenav argument` is the slug of the top level menu item e.g::

   {% load treenav_tags %}
   {% show_treenav 'primary-nav' %}

#. Apply CSS to your navigation by adding it to your base template and media
   directory using the classes described in :ref:`html-example`.


Override your templates
-----------------------

If you want to customize a menubar depending on the page a user visited you can do that.
The `show_treenav`, `single_level_menu` and `render_menu_children` now offer a fully
customize approach based on slugs of the nodes.

For example:

1. We have a menu that contains 4 items

- root (slug: 'root', link: '/')
- category1 (slug: 'category1', link: '/category', child of root)
- subcategory (slug: 'subcategory', link: '/category/subcategory', child of child1)
- category2 (slug: 'category2', link: '/category2', child of root)

For root node treenav will search for::

    [
        'treenav/root.html',
        'treenav/menuitem.html',
    ]

For category1::

    [
        'treenav/root/category1.html',
        'treenav/root/menuitem.html',
        'treenav/category1.html',
        'treenav/menuitem.html',
    ]

For subcategory::

    [
        'treenav/root/category1/subcategory.html',
        'treenav/root/category1/menuitem.html',
        'treenav/root/subcategory.html',
        'treenav/root/menuitem.html',
        'treenav/subcategory.html',
        'treenav/menuitem.html',
    ]

This way you can customize your menu depending on which page the user is.
Each template_path is build based on the node's slug and each parent's slug that the child
belongs to.
