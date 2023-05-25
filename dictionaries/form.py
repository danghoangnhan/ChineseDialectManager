from django import forms
from import_export.forms import ImportForm, ConfirmImportForm, ExportForm

from dictionaries.models import dictionary
from rules.models import ToneRules

tone_convert_type = [("BC_AT", "BC TO AT"), ("AT_BC", "AT TO BC")]
enable_tone_option = [("1", "yes"), ("2", "no")]


class VocabularyImportForm(ImportForm):
    dictionary_name = forms.ModelChoiceField(label="dictionary name", queryset=dictionary.objects.all(), required=True)
    tone_option = forms.ChoiceField(choices=lambda: [(element['country_type'], element['country_type']) for element in
                                                     ToneRules.objects.values('country_type').distinct()])


class DictionaryExportForm(ExportForm):
    tone_option = forms.ChoiceField(choices=lambda: [(element['country_type'], element['country_type']) for element in
                                                     ToneRules.objects.values('country_type').distinct()])

class VocabularyConfirmImportForm(ConfirmImportForm):
    dictionary_name = forms.ModelChoiceField(label="dictionary name", queryset=dictionary.objects.all())
