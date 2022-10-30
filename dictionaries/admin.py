from django.contrib import admin

from dictionaries.DictionaryAdmin import DictionaryAdmin
from dictionaries.VocabularyAdmin import VocabularyAdmin
from dictionaries.VocabularyModel import vocabulary
from dictionaries.models import dictionary

admin.register(vocabulary, VocabularyAdmin)
admin.register(dictionary, DictionaryAdmin)
