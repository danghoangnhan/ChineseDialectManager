from django import forms
from import_export.forms import ImportForm, ConfirmImportForm
from dictionary.models import dictionary


class ToneImportForm(ImportForm):
    dictionary_name = forms.ModelChoiceField(label="dictionary_name", queryset=dictionary.objects.all(), required=True)


class ToneConfirmImportForm(ConfirmImportForm):
    dictionary_name = forms.ModelChoiceField(label="dictionary_name", queryset=dictionary.objects.all(), required=True)
