from django.contrib import admin

from dictionaries.models import dictionary


@admin.register(dictionary)
class DictionaryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    change_list_template = "../templates/dictionaries/dictionary/change_list.html"