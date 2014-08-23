import random
import string

from django.test import TestCase

from treenav.models import MenuItem


class TreeNavTestCase(TestCase):
    "Base test case for creating TreeNav data."

    def get_random_string(self, length=10):
        return ''.join(random.choice(string.ascii_letters) for x in range(length))

    def create_menu_item(self, **kwargs):
        "Create a random MenuItem."
        defaults = {
            'label': self.get_random_string(),
            'slug': self.get_random_string(),
            'order': 0
        }
        defaults.update(kwargs)
        return MenuItem.objects.create(**defaults)
