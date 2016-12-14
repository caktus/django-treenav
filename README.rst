django-treenav
==============

.. sidebar:: Build Status

   :master: |master-status|
   :develop: |develop-status|
   :coverage: |coverage|

An extensible, hierarchical, and pluggable navigation system for Django sites.

*django-treenav* was designed from the start to live independent of a CMS
implementation. As a separate application, treenav can easily be integrated
into existing, custom setups and does not enforce or require users to use a
particular content management system.

Sharing the same principles,
`django-pagelets <http://readthedocs.org/projects/django-pagelets/>`_
integrates seamlessly with treenav and can be used together to create a flexible
CMS product.

For complete documentation checkout, `<http://django-treenav.readthedocs.org>`_

.. |master-status| image::
    https://travis-ci.org/caktus/django-treenav.svg?branch=master
    :target: https://travis-ci.org/caktus/django-treenav
    :alt: Master Build Status

.. |develop-status| image::
    https://travis-ci.org/caktus/django-treenav.svg?branch=develop
    :target: https://travis-ci.org/caktus/django-treenav
    :alt: Develop Build Status

.. |coverage| image::
    https://coveralls.io/repos/caktus/django-treenav/badge.png?branch=develop
    :target: https://coveralls.io/r/caktus/django-treenav


Features
--------

- Generic functionality with multiple URL specifications: `get_absolute_url()`, `reverse()`, or raw URLs
- Packaged with templates to render the tree hierarchy with nested `<ul>`'s, but can easily be overridden with custom templates
- Useful CSS classes for flexible UI customization
- Automatically sets "active" on item and item's parents if `PATH_INFO` is equal to `item.href`
- Efficient: minimizes database access with django-mptt functionality
- Caches the tree so that repeated page views do not hit the database.
- Simple links in the `MenuItem` list view for refreshing the cache and href
  from the database.

Requirements
------------
- `django <https://github.com/django/django/>`_ >= 1.8
- `django-mptt <http://github.com/django-mptt/django-mptt/>`_ >= 0.8.6

Using the demo
--------------

For a quick demo, follow these steps::

    $ mkvirtualenv django-treenav
    (django-treenav)$ git clone git://github.com/caktus/django-treenav.git
    (django-treenav)$ cd django-treenav/
    (django-treenav)~/django-treenav$ python setup.py develop
    (django-treenav)~/django-treenav$ cd sample_project/
    (django-treenav)~/django-treenav/sample_project$ pip install -r requirements.txt
    (django-treenav)~/django-treenav/sample_project$ ./manage.py migrate
    (django-treenav)~/django-treenav/sample_project$ ./manage.py runserver

Visit http://localhost:8000/ in your browser and follow the instructions.

Installation
------------

#. Install the app with pip::

    pip install django-treenav


#. Add to your `INSTALLED_APPS` and run migrate::

    INSTALLED_APPS = (
        ...,
        'mptt',
        'treenav',
    )


#. Include these context processors::

    TEMPLATES = [
      {
        'OPTIONS': {
          'context_processors': [
            "django.template.context_processors.request",
            "treenav.context_processors.treenav_active",
          ],
        },
      },
    ]

#. Add these urls::

    urlpatterns = [
        url(r'^treenav/', include('treenav.urls')),
    ]


Development sponsored by `Caktus Consulting Group, LLC
<http://www.caktusgroup.com/services/>`_.
