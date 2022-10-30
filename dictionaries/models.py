from django.db import models


class dictionary(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=100)

    class Meta:
        db_table = 'dictionary'
        verbose_name = 'Dictionary'
        verbose_name_plural = 'Dictionaries'

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name


