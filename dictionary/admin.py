import csv
from collections import defaultdict

from django.contrib import admin
from django.http import HttpResponse
from django_admin_row_actions import AdminRowActionsMixin
from django_object_actions import DjangoObjectActions
from import_export.admin import ExportActionMixin, ImportExportMixin, ImportExportActionModelAdmin
from import_export.formats.base_formats import DEFAULT_FORMATS

from dictionary.form import DictionaryExportForm
from dictionary.models import dictionary
from dictionary.resource import DictionaryAdminResource
from vocabulary.model import vocabulary


@admin.register(dictionary)
class DictionaryAdmin(DjangoObjectActions,
                      AdminRowActionsMixin,
                      ImportExportMixin,
                      ImportExportActionModelAdmin,
                      ExportActionMixin,
                      admin.ModelAdmin):
    list_display = ('name', 'description')
    actions = ['merge_duplicated_words']
    search_fields = ['name', 'description']
    export_form_class = DictionaryExportForm
    resource_class = DictionaryAdminResource
    list_per_page = 15

    @admin.action(description=' merge duplicated words')
    def merge_duplicated_words(self, request, queryset):
        header = ['字']
        template = ['音', '聲調', 'IPA']
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(vocabulary._meta)
        writer = csv.writer(response)
        datalist = [obj for obj in queryset]
        dictionary_list = set([getattr(obj, 'dictionary_name') for obj in datalist])
        mapping = defaultdict(dict)
        for data_element in datalist:
            if mapping.get(data_element) is None:
                mapping[getattr(data_element, 'word')] = defaultdict()
            mapping[getattr(data_element, 'word')][getattr(data_element, 'dictionary_name')] = data_element

        for dictionary_name in dictionary_list:
            for col in template:
                header.append(dictionary_name + '_' + col)
        writer.writerow(header)
        for key in mapping:
            rowValue = [key]
            inode = mapping.get(key)
            for dictionary_name in dictionary_list:
                obj = inode.get(dictionary_name)
                if obj is not None:
                    rowValue.append(getattr(obj, 'word'))
                    rowValue.append(getattr(obj, 'tone'))
                    rowValue.append(getattr(obj, 'ipa'))
                else:
                    rowValue.append(None)
                    rowValue.append(None)
                    rowValue.append(None)
            writer.writerow(rowValue)
        return response

    def get_resource_kwargs(self, request, *args, **kwargs):
        rk = super().get_resource_kwargs(request, *args, **kwargs)
        file_format_id = int(request.POST.get('file_format'))
        rk['file_format'] = DEFAULT_FORMATS[file_format_id - 1].CONTENT_TYPE
        rk['tone_option'] = request.POST.get('tone_option')
        rk['checkbox_field'] = request.POST.getlist('checkbox_field')
        return rk
