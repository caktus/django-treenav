Setup
=====

.. highlight:: html+django
#. Login to the admin and build your menu item hierarchy
#. Load the treenav_tags in your template and render the menu where the 
   show_treenav argument is the slug of the top level menu item e.g.

    ::

        {% load treenav_tags %}
        {% show_treenav 'primary-nav' %}

    .. highlight:: python

#. Add treenav urls into your url patterns, e.g.

    ::

        (r'^%streenav/' % settings.URL_PREFIX, include('treenav.urls.admin')),
