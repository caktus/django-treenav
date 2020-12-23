django-treenav
==============

.. sidebar:: Build Status

   :master: |master-status|
   :develop: |develop-status|

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
    https://github.com/caktus/django-treenav/workflows/lint-test/badge.svg?branch=master
    :alt: Build Status
    :target: https://github.com/caktus/django-treenav/actions?query=branch%3Amaster

.. |develop-status| image::
    https://github.com/caktus/django-treenav/workflows/lint-test/badge.svg?branch=develop
    :alt: Build Status
    :target: https://github.com/caktus/django-treenav/actions?query=branch%3Adevelop


Features
--------

- Generic functionality with multiple URL specifications: `get_absolute_url()`, `reverse()`, or raw URLs
- Packaged with templates to render the tree hierarchy with nested `<ul>`'s, but can easily be overridden with custom templates
- Easily customize each item's template or fall back to a default `menuitem.html`
- Useful CSS classes for flexible UI customization
- Automatically sets "active" on item and item's parents if `PATH_INFO` is equal to `item.href`
- Efficient: minimizes database access with django-mptt functionality
- Caches the tree so that repeated page views do not hit the database.
- Simple links in the `MenuItem` list view for refreshing the cache and href
  from the database.

Requirements
------------

- `django <https://github.com/django/django/>`_ >= 2.2
- `django-mptt <https://github.com/django-mptt/django-mptt/>`_ >= 0.11.0

Using the demo
--------------

For a quick demo, follow these steps:

1. Create a virtualenv. (This example uses ``mkvirtualenv``, but there are many other
   ways to do it)::

     $ mkvirtualenv django-treenav

#. Check out the code and install the requirements::

     (django-treenav)$ git clone git://github.com/caktus/django-treenav.git
     (django-treenav)$ cd django-treenav/
     (django-treenav)~/django-treenav/$ pip install -Ur dev-requirements.txt

#. Run migrations and create a superuser so you can login to the Django admin::

     (django-treenav)~/django-treenav$ python manage.py migrate
     (django-treenav)~/django-treenav$ python manage.py createsuperuser

#. Run the server::

     (django-treenav)~/django-treenav$ python manage.py runserver

#. Visit http://localhost:8000/ in your browser and follow the instructions.


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


Maintainer Information
----------------------

We use Github Actions to lint (using pre-commit, black, isort, and flake8),
test (using tox and tox-gh-actions), calculate coverage (using coverage), and build
documentation (using sphinx).

We have a local script to do these actions locally, named ``maintain.sh``::

  $ ./maintain.sh

A Github Action workflow also builds and pushes a new package to PyPI whenever a new
Release is created in Github. This uses a project-specific PyPI token, as described in
the `PyPI documentation here <https://pypi.org/help/#apitoken>`_. That token has been
saved in the ``PYPI_PASSWORD`` settings for this repo, but has not been saved anywhere
else so if it is needed for any reason, the current one should be deleted and a new one
generated.

As always, be sure to bump the version in ``treenav/__init__.py`` before creating a
Release, so that the proper version gets pushed to PyPI.


Development sponsored by `Caktus Consulting Group, LLC
<https://www.caktusgroup.com/services/>`_.
