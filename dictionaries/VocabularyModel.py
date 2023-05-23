from django.db import models


class vocabulary(models.Model):
    # id = models.AutoField(primary_key=True)
    word = models.CharField(max_length=50, db_column='word')
    tone = models.CharField(max_length=5, db_column='tone')
    symbol_text = models.CharField(max_length=50, db_column='symbol_text')
    dictionary_name = models.CharField(max_length=5, db_column='dictionary_name')
    ipa = models.CharField(max_length=5, db_column='ipa')
    description = models.CharField(max_length=1000, db_column='description')

    class Meta:
        db_table = 'vocabulary'
        verbose_name = 'Vocabulary'
        verbose_name_plural = 'vocabularies'

    def __str__(self):
        return self.word
