Release History
====================================

Release and change history for django-treenav


v0.9.0 (Released 2012-10-26)
------------------------------------

This release is a clean up release for the API and internals. This should be
considered a release candidate for an offical v1.0.

- Dropped support for Django prior to 1.3
- Added tox support for testing

Backwards Incompatible Changes
___________________________________

- ``treenav_refresh_hrefs`` and ``treenav_clean_cache`` were moved under the admin and require staff access
- Including url patterns has been simplified and ``treenav.urls.admin`` were removed


0.6.1 (Released 2012-04-12)
------------------------------------

- Fixed bug that prevented adding parent and child menu items simultaneously


0.6.0 (Released 2011-12-02)
------------------------------------
- Moved to GitHub
- Add Sphinx-powered documentation
- Update to Django 1.3.x and django-mptt 0.5.2
- Provide more order choices by default
- Fix a few documentation related bugs
- Cleaned up sample project for an easier demo


0.5.0 (Released 2011-03-11)
------------------------------------

- Initial release
