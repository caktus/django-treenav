from django.db import models


class Team(models.Model):
    name = models.CharField(max_length=20)
    
    def get_absolute_url(self):
        return '/team/%d/' % self.pk
