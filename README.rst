django-treenav
==============

Extensible, hierarchical, and pluggable navigation system for Django sites.

Doing a simple search will show you that django has a number of dynamic
menu generation systems, so why did we build another one?  Many of the projects
that existed before treenav had a tight coupling with the content, typically a
CMS.

Along side of treenav we built the first versions of `django-pagelets
<http://readthedocs.org/projects/django-pagelets/>`_
.  We opted to build two seperate apps so that we weren't using both when one 
or the other wasn't useful.

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
  <http://github.com/django-mptt/django-mptt/>`_
  *should be installed from the github repository instead of pip until 
  django-mptt releases a version later than 4.2 to avoid having errors in the
  ordering of menu items.*

Installation
------------

.. highlight:: python    

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
