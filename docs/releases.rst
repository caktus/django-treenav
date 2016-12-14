Release History
====================================

Release and change history for django-treenav

vNEXT (Released DATE)
---------------------

- To be determined


v1.1.0 (Released 2016-12-14)
------------------------------------

- Django 1.9 and 1.10 support (#67)
- Dropped support for Django 1.7


v1.0.0 (Released 2015-10-01)
------------------------------------

This is a stable release supporting Django 1.8 and Python 3.

- Python 3 support (#28)
- Django 1.8 support (#40)
- Confirmed support for django-mptt 0.7
- Confirmed support for Django 1.7
- Dropped support for Django prior to 1.7
- Dropped support for Python 2 prior to 2.7
- Dropped support for Python 3 prior to 3.3
- Dropped support for django-mptt prior to 0.7
- Setup Travis (#27)
- Add docs for 'Rebuild Tree' admin action.
- Updated Tox (#45) and Travis (#50) to work with Tox 2.0
- Updated sample project to work with Django 1.8 and django-mptt 0.7 (#25)
- Fixed bug that prevented deletion of items from admin changelist (#54)
- Fixed bug where reordering items in the admin would disorder tree (#42)
- Switched to Django migrations (#63)

Backwards Incompatible Changes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- ``MenuItem`` model no longer uses ``.tree`` for ``TreeManager`` methods. Instead use ``.objects`` (change from django-mptt 0.5)
- If you are upgrading from 0.9.2 (or earlier) and are currently using Django 1.8, then you will need to
  run ``python manage.py migrate --fake-initial`` since we have converted from using South to Django
  migrations. Django 1.7 does "fake-initial" behavior by default.
- The ``post_save`` signal which updates MenuItems when their corresponding object changes will NOT
  be active during data migrations. If you update any objects during a data migration, and that
  object has a corresponding MenuItem, you will need to manually update the HREF of the MenuItem.

v0.9.2 (Released 2015-09-02)
------------------------------------

- Add 'Rebuild Tree' button for MenuItem admin

v0.9.1 (Released 2012-10-26)
------------------------------------

- Allow MenuItem.parent to be blank
- Fixed bug that prevented display of more than 2 levels of tree when ``full_tree`` was set to True

v0.9.0 (Released 2012-10-26)
------------------------------------

This release is a clean up release for the API and internals. This should be
considered a release candidate for an offical v1.0.

- Dropped support for Django prior to 1.3
- Added tox support for testing

Backwards Incompatible Changes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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
