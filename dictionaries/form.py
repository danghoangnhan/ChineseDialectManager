from django import forms
from import_export.forms import ImportForm, ConfirmImportForm, ExportForm

from dictionaries.models import dictionary
from rules.models import ToneRules

tone_convert_type = [("B_C", "Chinese"), ("A_T", "Taiwan")]
enable_tone_option = [("1", "yes"), ("2", "no")]


class VocabularyImportForm(ImportForm):
    dictionary_name = forms.ModelChoiceField(label="dictionary name", queryset=dictionary.objects.all(), required=True)
    tone_option = forms.ChoiceField(choices=lambda: tone_convert_type)


class DictionaryExportForm(ExportForm):
    tone_option = forms.ChoiceField(choices=lambda: tone_convert_type)
    checkbox_field = forms.MultipleChoiceField(
        label="select dictionary",
        widget=forms.CheckboxSelectMultiple,
        choices=lambda: [(obj.id, obj.name) for obj in dictionary.objects.all()]
    )


class VocabularyExportForm(ExportForm):
    tone_option = forms.ChoiceField(choices=lambda: tone_convert_type)
    checkbox_field = forms.MultipleChoiceField(
        label="select dictionary",
        widget=forms.CheckboxSelectMultiple,
        choices=lambda: [(obj.id, obj.name) for obj in dictionary.objects.all()]
    )


class VocabularyConfirmImportForm(ConfirmImportForm):
    dictionary_name = forms.ModelChoiceField(label="dictionary name", queryset=dictionary.objects.all())
