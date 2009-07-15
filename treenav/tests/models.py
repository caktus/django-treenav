from django.db import models


class Team(models.Model):
    slug = models.SlugField()
    
    def get_absolute_url(self):
        return '/team/%s/' % self.slug
