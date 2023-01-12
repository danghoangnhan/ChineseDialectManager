from django.db import models
from django.db.models import ForeignKey
from django.forms import JSONField
from dictionaries.models import dictionary


class rules(models.Model):
    name = models.CharField(max_length=50, unique=True)
    unicode_repr = models.CharField(max_length=100, unique=False)
    descriptors = models.CharField(max_length=100, unique=False)
    dictionary = ForeignKey(dictionary, on_delete=models.CASCADE, default=None, related_name='dictionary',db_column='dictionary')
    type = models.CharField(max_length=100, unique=False)

    class Meta:
        db_table = 'rules'
        verbose_name = 'Rules'
        verbose_name_plural = 'Rules'

    args = JSONField()

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name
