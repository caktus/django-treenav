django-treenav
==============

Extensible, hierarchical, and pluggable navigation system for Django sites

.. highlight:: python

Features
--------

- Generic functionality with multiple URL specifications: get_absolute_url(), reverse(), or raw URLs
- Packaged with templates to render the tree hierarchy with nested `<ul>`'s, but can easily be overridden with custom templates
- Useful css classes for flexible UI customization
- Automatically sets "active" on item and item's parents if PATH_INFO is equal to item.href
- Efficient: minimizes database access with django-mptt functionality

Requirements
------------
- `django
  <https://github.com/django/django/>`_
- `django-mptt
  <http://code.google.com/p/django-mptt/>`_

Installation
------------
#.  Install the app with pip::

        pip install django-treenav


#. Add to your INSTALLED_APPS and run syncdb::

        INSTALLED_APPS = (
            ...,
            'mptt',
            'treenav',
        )


#. Include these context processors::

    TEMPLATE_CONTEXT_PROCESSORS = (
        "django.core.context_processors.request",
        "treenav.context_processors.treenav_active",
    )


#. Add these urls::

    urlpatterns = patterns('',
        (r'^treenav/', include('treenav.urls.admin')),
        (r'^treenav-missing/', include('treenav.urls.undefined_url')),
    )
    
Development sponsored by `Caktus Consulting Group, LLC
<http://www.caktusgroup.com/services>`_.
