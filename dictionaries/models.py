from django.db import models
from django.forms import JSONField

tone_convert_type = [("BC", "BC"), ("AT", "AT")]
enable_tone_option = [("1", "yes"), ("2", "no")]


class dictionary(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=100)
    args = JSONField()

    class Meta:
        db_table = 'dictionary'
        verbose_name = 'Dictionary'
        verbose_name_plural = 'Dictionaries'


    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name


class tone_convert(models.Model):
    country_type = models.CharField(max_length=50)
    description = models.CharField(max_length=100)
    flat = models.IntegerField()
    up = models.IntegerField()
    go = models.IntegerField()
    into = models.IntegerField()
    type = models.CharField(max_length=100)

    class Meta:
        db_table = 'tone_rule'
        verbose_name = 'Tone_rule'
        verbose_name_plural = 'tone_rules'

    args = JSONField()

    def __unicode__(self):
        return self.country_type

    def __str__(self):
        return self.country_type
