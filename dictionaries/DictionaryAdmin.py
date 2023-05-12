from django.contrib import admin

from dictionaries.models import dictionary


@admin.register(dictionary)
class DictionaryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'enable_tone_convert', 'convert_type')
    list_editable = ('enable_tone_convert', 'convert_type')
    change_list_template = "../templates/dictionaries/dictionary/change_list.html"
