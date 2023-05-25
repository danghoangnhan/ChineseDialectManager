import csv
from collections import defaultdict

from django.contrib import admin
from django.http import HttpResponse
from django_admin_row_actions import AdminRowActionsMixin
from django_object_actions import DjangoObjectActions
from import_export.admin import ExportActionMixin, ImportExportMixin, ImportExportActionModelAdmin

from dictionaries.VocabularyModel import vocabulary
from dictionaries.form import DictionaryExportForm
from dictionaries.models import dictionary


@admin.register(dictionary)
class DictionaryAdmin(DjangoObjectActions,
                      AdminRowActionsMixin,
                      ImportExportMixin,
                      ImportExportActionModelAdmin,
                      ExportActionMixin,
                      admin.ModelAdmin):
    list_display = ('name', 'description', 'input_tone', 'output_tone')
    list_editable = ('input_tone', 'output_tone')
    # change_list_template = "..dictionaries/dictionary/change_list.html"
    actions = ['merge_duplicated_words']
    export_form_class = DictionaryExportForm

    # class Media:
    #     js = ('../static/dictionary/dictionary_admin.js',)  # Path to your JavaScript file

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = super().get_readonly_fields(request, obj)
        if obj and not obj.enable_tone_convert:
            readonly_fields += ('convert_type',)
        return readonly_fields

    def changeform_view(self, request, *args, **kwargs):
        self.readonly_fields = list(self.readonly_fields)
        usergroup = request.user.groups.filter(name__in=['author']).exists()
        if not usergroup:
            self.readonly_fields.append('price_upgrade')

        return super(DictionaryAdmin, self).changeform_view(request, *args, **kwargs)

    @admin.action(description=' merge duplicated words')
    def merge_duplicated_words(self, request, queryset):
        header = ['字']
        template = ['音', '聲調', 'IPA']
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(vocabulary._meta)
        writer = csv.writer(response)
        v = defaultdict(dict)
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
