from import_export.admin import ImportExportModelAdmin
from django.contrib import admin
from apps.dictionary.models import Dictionary


@admin.register(Dictionary)
class DictionaryAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    ...
