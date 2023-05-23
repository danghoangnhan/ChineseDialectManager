from django.db import models
from django.forms import JSONField

from dictionaries.models import dictionary


class ToneRules(models.Model):
    country_type = models.CharField(max_length=255, db_column='country_type', null=True)
    flat = models.IntegerField(db_column='flat', null=True)
    up = models.IntegerField(db_column='up', null=True)
    go = models.IntegerField(db_column='go', null=True)
    into = models.IntegerField(db_column='into', null=True)
    type = models.CharField(max_length=255, db_column='type', null=True)

    class Meta:
        db_table = 'tone_rules'
    def __unicode__(self):
        return self.country_type

    def __str__(self):
        return self.country_type


class rules(models.Model):
    name = models.CharField(max_length=50, unique=True)
    unicode_repr = models.CharField(max_length=100, unique=False)
    descriptors = models.CharField(max_length=100, unique=False)
    dictionary_name = models.CharField(max_length=50)
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
