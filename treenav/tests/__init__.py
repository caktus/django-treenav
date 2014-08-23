# flake8: noqa
from django.db import models

# per http://code.djangoproject.com/ticket/7835#comment:24,
# include test model in tests.py (until there's a better way)
# it does NOT work to include it in a separate file and import it here,
# because the app label will be incorrect.  See:
#   * http://code.djangoproject.com/ticket/4470 (closed as a dup) and
#   * http://code.djangoproject.com/ticket/3591
class Team(models.Model):

    slug = models.SlugField()

    def get_absolute_url(self):
        return '/team/%s/' % self.slug

from .test_models import TreeOrder
from .test_views import TreeNavTestCase, TreeNavViewTestCase
from .test_views import RefreshViewTestCase, ClearCacheViewTestCase
