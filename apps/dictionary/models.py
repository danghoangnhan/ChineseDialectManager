from django.db import models


class Dictionary(models.Model):
    Symbol = models.CharField(max_length=30)
    Tone = models.CharField(max_length=30)
    Word = models.CharField(max_length=60)
    ipa = models.EmailField(blank=True)

    def __str__(self):
        return self.Symbol
