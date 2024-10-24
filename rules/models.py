from django.db import models
from django.forms import JSONField

from dictionary.models import dictionary


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
    name = models.CharField(max_length=50)
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


def tone_encode_mapper(country_type):
    tone_rules = ToneRules.objects.filter(country_type=country_type)
    type_mappings = {}
    for tone_rule in tone_rules:
        type_mappings[int(tone_rule.flat)] = (tone_rule.type, "flat")
        type_mappings[int(tone_rule.up)] = (tone_rule.type, "up")
        type_mappings[int(tone_rule.go)] = (tone_rule.type, "go")
        type_mappings[int(tone_rule.into)] = (tone_rule.type, "into")
    return type_mappings


def tone_decode_mapper(country_type):
    tone_rules = ToneRules.objects.filter(country_type=country_type)
    type_mappings = {}

    for tone_rule in tone_rules:
        type_mappings[(tone_rule.type, "flat")] = int(tone_rule.flat)
        type_mappings[(tone_rule.type, "up")] = int(tone_rule.up)
        type_mappings[(tone_rule.type, "go")] = int(tone_rule.go)
        type_mappings[(tone_rule.type, "into")] = int(tone_rule.into)
    return type_mappings


def convert_tone(tone_original: int, tone_encoder, tone_decoder):
    try:
        tone_original = int(tone_original)
        if tone_original in tone_encoder:
            key1, key2 = tone_encoder.get(tone_original)
            return tone_decoder.get((key1, key2), -1)
    except Exception as e:
        pass  # You can optionally print or log the exception for debugging purposes
    return -1
