import csv

from django.contrib import admin
from django.http import HttpResponse

from apps.dictionary.models import models
from apps.dictionary.models import Dictionary


# Code from http://books.agiliq.com/projects/django-admin-cookbook/en/latest/export.html
class ExportCsvMixin:
    """ Admin Mixin to export CSV"""

    def export_as_csv(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            writer.writerow([getattr(obj, field) for field in field_names])

        return response

    export_as_csv.short_description = "Export Selected"


class DictionaryAdmin(admin.ModelAdmin):
    list_display = ('site_id', 'warming_start', 'ecosystem_type')
    list_filter = ('ecosystem_type',)
    search_fields = ('site_id',)

    fieldsets = (
        ('Site Information', {
            'fields': ('site_id', 'warming_start', 'ecosystem_type')
        }),
        ('Soil Information', {
            'fields': (('sand_pct', 'silt_pct', 'clay_pct'),),
        }),
    )

    class Media:
        css = {
            "screen": ("csv_example/css/admin.css",)
        }


# Register your models here.
admin.site.register(Dictionary, DictionaryAdmin)
