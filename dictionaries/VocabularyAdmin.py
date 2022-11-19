from django import forms as form_2
from django.contrib.auth.admin import admin
from django_admin_row_actions import AdminRowActionsMixin
from django_object_actions import DjangoObjectActions
from import_export.admin import ExportActionMixin, ImportExportMixin, ImportExportActionModelAdmin
from import_export.forms import ImportForm, ConfirmImportForm

from consonant import Dictionary
from dictionaries.VocabularyModel import vocabulary
from dictionaries.form import VocabularyImportForm, VocabularyConfirmImportForm
from dictionaries.models import dictionary
from dictionaries.resource import VocabularyAdminResource

chaoshan = Dictionary()


class VocabularyInline(admin.StackedInline):
    model = vocabulary


class CustomImportForm(ImportForm):
    author = form_2.ModelChoiceField(
        queryset=dictionary.objects.all(),
        required=True)


class CustomConfirmImportForm(ConfirmImportForm):
    dictionary_name = form_2.ModelChoiceField(
        queryset=dictionary.objects.all(),
        required=True)


@admin.register(vocabulary)
class VocabularyAdmin(DjangoObjectActions,
                      AdminRowActionsMixin,
                      ImportExportMixin,
                      ImportExportActionModelAdmin,
                      ExportActionMixin,
                      admin.ModelAdmin):
    list_display = ('symbol_text', 'word', 'tone', 'ipa', 'description', 'dictionary_name')
    list_filter = ("dictionary_name",)
    search_fields = ("dictionary_name",)
    actions = ['update_ipa']
    change_list_template = "../templates/dictionaries/dictionary/change_list.html"
    resource_class = VocabularyAdminResource
    import_form_class = VocabularyImportForm
    confirm_form_class = VocabularyConfirmImportForm

    def get_resource_kwargs(self, request, *args, **kwargs):
        rk = super().get_resource_kwargs(request, *args, **kwargs)
        # This method may be called by the initial form GET request, before
        # the contract is chosen. So we default to None.
        rk['dictionary_name'] = None
        if request.POST:  # *Now* we should have a non-null value
            # In the dry-run import, the contract is included as a form field.
            dictionary_name = request.POST.get('dictionary_name', None)
            if dictionary_name:
                # If we have it, save it in the session so we have it for the confirmed import.
                request.session['dictionary_name'] = dictionary_name
            else:
                try:
                    # If we don't have it from a form field, we should find it in the session.
                    dictionary_name = request.session['dictionary_name']
                except KeyError as e:
                    raise Exception("Context failure on row import, " +
                                    f"check admin.py for more info: {e}")
            rk['dictionary_name'] = dictionary_name
        return rk

    @admin.action(description='Update the IPA')
    def update_ipa(self, request, obj):
        request.POST.getlist(admin.ModelAdmin)


def generateVocabulary(data) -> vocabulary:
    fields = data.replace('\r', '').split(",")
    result = vocabulary(
        symbol_text=fields[0],
        word=str(fields[1]).lower(),
        tone=fields[2],
        ipa=chaoshan.chaoshan2IPA(str(fields[1]).lower()),
        description='',
        dictionary_name=dictionary.objects.get(name__contains='潮汕')
    )
    return result
