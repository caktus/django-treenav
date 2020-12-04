from django.db import models


class Team(models.Model):

    slug = models.SlugField()

    def get_absolute_url(self):
        """Return an hard-coded URL pattern for this model."""
        return f"/team/{self.slug}/"
