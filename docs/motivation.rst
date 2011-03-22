Motivation
==========

Doing a simple search will show you that django has a number of dynamic
menu generation systems, so why did we build another one?  Many of the projects
that existed before treenav had a tight coupling with the content, typically a
CMS.

Along side of treenav we built the first versions of `django-pagelets
<http://readthedocs.org/projects/django-pagelets/>`_
.  We opted to build two seperate apps so that we weren't using both when one 
or the other wasn't useful.

Treenav is capable of linking to  named urls, any model object with 
get_abosolute_url defined, and even to pages on different sites.
