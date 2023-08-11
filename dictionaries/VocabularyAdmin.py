from django.contrib.auth.admin import admin
from django_admin_row_actions import AdminRowActionsMixin
from django_object_actions import DjangoObjectActions
from import_export.admin import ExportActionMixin, ImportExportMixin, ImportExportActionModelAdmin

from dictionaries.VocabularyModel import vocabulary
from dictionaries.form import VocabularyImportForm, VocabularyExportForm
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
    search_fields = ['symbol_text', 'word', 'tone', 'ipa', 'dictionary_name']
    actions = ['export_as_csv']
    # change_list_template = "../templates/dictionaries/vocabulary/change_list.html"
    resource_class = VocabularyAdminResource
    import_form_class = VocabularyImportForm
    # confirm_form_class = VocabularyConfirmImportForm
    cache = {}
    list_filter = ['dictionary_name']
    export_form_class = VocabularyExportForm


    def get_resource_kwargs(self, request, *args, **kwargs):
        rk = super().get_resource_kwargs(request, *args, **kwargs)
        if 'dictionary_name' not in self.cache:
            if request.POST.get('dictionary_name') is not None:
                self.cache['dictionary_name'] = request.POST.get('dictionary_name')
        if 'tone_option' not in self.cache:
            if request.POST.get('tone_option') is not None:
                self.cache['tone_option'] = request.POST.get('tone_option')

        rk['dictionary_name'] = self.cache['dictionary_name'] if 'dictionary_name' in self.cache else request.POST.get(
            'dictionary_name')
        rk['tone_option'] = self.cache['tone_option'] if 'tone_option' in self.cache else request.POST.get(
            'tone_option')
        return rk
