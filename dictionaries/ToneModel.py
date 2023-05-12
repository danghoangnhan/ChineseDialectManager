from django.db import models


class vocabulary(models.Model):
    country_type = models.CharField()
    flat = models.IntegerField()
    up = models.IntegerField()
    go = models.IntegerField()
    into = models.IntegerField()
    type = models.CharField()

    class Meta:
        db_table = 'tone_rules'
        verbose_name = 'tone_rules'
        verbose_name_plural = 'tone_rules'

    def __str__(self):
        return self.word