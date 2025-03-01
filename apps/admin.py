from django.contrib import admin

from dictionary.models import dictionary
from dictionary.admin import DictionaryAdmin
from vocabulary.model import vocabulary
from vocabulary.admin import VocabularyAdmin


admin.site.register(dictionary, DictionaryAdmin)
admin.site.register(vocabulary, VocabularyAdmin)
