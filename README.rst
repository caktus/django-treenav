django-treenav
==============

An extensible, hierarchical, and pluggable navigation system for Django sites.

*django-treenav* was designed from the start to live independent of a CMS
implementation. As a separate application, treenav can easily be integrated
into existing, custom setups and does not enforce or require users to use a
particular content management system.

Sharing the same principals,
`django-pagelets <http://readthedocs.org/projects/django-pagelets/>`_
integrates seamlessly with treenav and can be used together to create a flexible
CMS product.

For complete documentation checkout, `<http://django-treenav.readthedocs.org>`_

Features
--------

- Generic functionality with multiple URL specifications: `get_absolute_url()`, `reverse()`, or raw URLs
- Packaged with templates to render the tree hierarchy with nested `<ul>`'s, but can easily be overridden with custom templates
- Useful CSS classes for flexible UI customization
- Automatically sets "active" on item and item's parents if `PATH_INFO` is equal to `item.href`
- Efficient: minimizes database access with django-mptt functionality
- Caches the tree so that repeated page views to not hit the database.
- Simple links in the `MenuItem` list view for refreshing the cache and href
  from the database.

Requirements
------------
- `django
  <https://github.com/django/django/>`_
- `django-mptt
  <http://github.com/django-mptt/django-mptt/>`_

  Version 4.2 and lower contains a `bug <https://github.com/django-mptt/django-mptt/issues#issue/14>`_
  that causes children menu items to become out of order when saved as a formset
  in Django's admin interface.

  This issue has been resolved in the latest development version of django-mptt,
  which can be installed with::

   pip install -e git+https://github.com/django-mptt/django-mptt.git#egg=django-mptt


Installation
------------

.. highlight:: python

#. Install the app with pip::

    pip install django-treenav


#. Add to your `INSTALLED_APPS` and run syncdb::

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

