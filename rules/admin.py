from django import forms as form_2
from django.contrib.auth.admin import admin
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

    change_list_template = "../templates/dictionaries/dictionary/change_list.html"
    resource_class = RulesResource
    import_form_class = VocabularyImportForm

    # confirm_form_class = VocabularyConfirmImportForm

    def get_resource_kwargs(self, request, *args, **kwargs):
        rk = super().get_resource_kwargs(request, *args, **kwargs)
        rk['dictionary_name'] = None
        if request.POST:  # *Now* we should have a non-null value
            dictionary_name = request.POST.get('dictionary_name', None)
            if dictionary_name:
                request.session['dictionary_name'] = dictionary_name
            else:
                try:
                    dictionary_name = request.session['dictionary_name']
                except KeyError as e:
                    raise Exception("Context failure on row import, " +
                                    f"check admin.py for more info: {e}")
            rk['dictionary_name'] = dictionary_name
        return rk
