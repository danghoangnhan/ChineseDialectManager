import csv
from collections import defaultdict

from django.contrib.auth.admin import admin
from django.http import HttpResponse
from django_admin_row_actions import AdminRowActionsMixin
from django_object_actions import DjangoObjectActions
from import_export.admin import ExportActionMixin, ImportExportMixin, ImportExportActionModelAdmin

from dictionaries.VocabularyModel import vocabulary
from dictionaries.form import VocabularyImportForm, VocabularyConfirmImportForm
from dictionaries.resource import VocabularyAdminResource


class VocabularyInline(admin.StackedInline):
    model = vocabulary


@admin.register(vocabulary)
class VocabularyAdmin(DjangoObjectActions,
                      AdminRowActionsMixin,
                      ImportExportMixin,
                      ImportExportActionModelAdmin,
                      ExportActionMixin,
                      admin.ModelAdmin):
    list_display = ('symbol_text', 'word', 'tone', 'ipa', 'dictionary_name')
    actions = ['export_as_csv']
    # change_list_template = "../templates/dictionaries/vocabulary/change_list.html"
    resource_class = VocabularyAdminResource
    import_form_class = VocabularyImportForm
    confirm_form_class = VocabularyConfirmImportForm

    @admin.action(description=' export to dictionary format csv')
    def export_as_csv(self, request, queryset):
        meta = vocabulary._meta
        header = ['字']
        template = ['音', '聲調', 'IPA']
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
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

    def get_resource_kwargs(self, request, *args, **kwargs):
        rk = super().get_resource_kwargs(request, *args, **kwargs)
        rk['dictionary_name'] = request.POST.get('dictionary_name')
        rk['tone_option'] = request.POST.get('tone_option')
        return rk
