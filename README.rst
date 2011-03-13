django-treenav
==============

Extensible, hierarchical, and pluggable navigation system for Django sites

Features
========

- Generic functionality with multiple URL specifications: get_absolute_url(), reverse(), or raw URLs
- Packaged with templates to render the tree hierarchy with nested `<ul>`'s, but can easily be overridden with custom templates
- Useful css classes for flexible UI customization
- Automatically sets "active" on item and item's parents if PATH_INFO is equal to item.href
- Efficient: minimizes database access with django-mptt functionality

Requirements
============
- `django-mptt
  <http://code.google.com/p/django-mptt/>`_

Installation
============
1) Download the app from GitHub and add it to your Python path:

::

    git clone git://github.com/caktus/django-treenav.git

2) Add to your INSTALLED_APPS and run syncdb

::

    INSTALLED_APPS = (
        ...,
        'mptt',
        'treenav',
    )


Setup
=====
1) Login to the admin and build your menu item hierarchy
2) Load the treenav_tags in your template and render the menu, e.g.

    ::

        {% load treenav_tags %}
        {% show_treenav 'primary-nav' %}


3) Add treenav urls into your url patterns, e.g.

    ::

        (r'^%streenav/' % settings.URL_PREFIX, include('treenav.urls.admin')),

Development sponsored by `Caktus Consulting Group, LLC
<http://www.caktusgroup.com/services>`_.
