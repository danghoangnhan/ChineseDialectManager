from django import forms
from import_export.forms import ImportForm, ConfirmImportForm

from dictionaries.models import dictionary


class VocabularyImportForm(ImportForm):
    dictionary_name = forms.ModelChoiceField(label="dictionary_name", queryset=dictionary.objects.all(), required=True)


# class VocabularyConfirmImportForm(ConfirmImportForm):
#     dictionary_name = forms.ModelChoiceField(label="dictionary_name", queryset=dictionary.objects.all(), required=True)
