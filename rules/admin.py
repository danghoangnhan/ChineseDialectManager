import os

from django import forms as form_2
from django.contrib.auth.admin import admin
from django.http import HttpResponseRedirect, HttpResponse
from django_admin_row_actions import AdminRowActionsMixin
from django_object_actions import DjangoObjectActions
from import_export.admin import ExportActionMixin, ImportExportMixin, ImportExportActionModelAdmin
from import_export.forms import ImportForm, ConfirmImportForm

from dictionaries.form import VocabularyImportForm
from rules.models import rules
from rules.resource import RulesResource


class RulesInline(admin.StackedInline):
    model = rules


class CustomImportForm(ImportForm):
    author = form_2.ModelChoiceField(
        queryset=rules.objects.all(),
        required=True)


class CustomConfirmImportForm(ConfirmImportForm):
    dictionary_name = form_2.ModelChoiceField(
        queryset=rules.objects.all(),
        required=True)


@admin.register(rules)
class RulesAdmin(DjangoObjectActions,
                 AdminRowActionsMixin,
                 ImportExportMixin,
                 ImportExportActionModelAdmin,
                 ExportActionMixin,
                 admin.ModelAdmin):
    list_display = ('name', 'descriptors', 'unicode_repr', 'dictionary', 'type')
    list_filter = ("dictionary",)
    search_fields = ("dictionary",)
    list_filter = ("dictionary",)
    search_fields = ("dictionary",)
    actions = ['export_as_csv']

    change_list_template = '../templates/rules/change_list.html'
    resource_class = RulesResource
    import_form_class = VocabularyImportForm
    # confirm_form_class = VocabularyConfirmImportForm

    def set_immortal(self, request):
        path = '../static/dictionary_rules.xlsx'  # this should live elsewhere, definitely
        if os.path.exists(path):
            with open(path, "r") as excel:
                data = excel.read()
            response = HttpResponse(data,
                                    content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = 'attachment; filename=%s_Report.xlsx' % id
            return response
        return HttpResponseRedirect(".")