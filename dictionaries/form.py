from django import forms
from import_export.forms import ImportForm, ConfirmImportForm

from dictionaries.models import dictionary

tone_convert_type = [("BC_AT", "BC TO AT"), ("AT_BC", "AT TO BC")]
enable_tone_option = [("1", "yes"), ("2", "no")]


class VocabularyImportForm(ImportForm):
    dictionary_name = forms.ModelChoiceField(label="dictionary_name", queryset=dictionary.objects.all(), required=True)


class VocabularyConfirmImportForm(ConfirmImportForm):
    dictionary_name = forms.ModelChoiceField(label="dictionary_name", queryset=dictionary.objects.all(), required=True)
