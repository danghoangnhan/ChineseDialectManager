from django import forms
from import_export.forms import ConfirmImportForm, ExportForm, ImportForm

from dictionary.form import tone_convert_type
from dictionary.models import dictionary


class VocabularyImportForm(ImportForm):
    dictionary_name = forms.ModelChoiceField(label="dictionary name", queryset=dictionary.objects.all(), required=True)
    tone_option = forms.ChoiceField(choices=lambda: tone_convert_type)


class VocabularyExportForm(ExportForm):
    tone_option = forms.ChoiceField(choices=lambda: tone_convert_type)
    checkbox_field = forms.MultipleChoiceField(
        label="select dictionary",
        widget=forms.CheckboxSelectMultiple,
        choices=lambda: [(obj.id, obj.name) for obj in dictionary.objects.all()]
    )


class VocabularyConfirmImportForm(ConfirmImportForm):
    dictionary_name = forms.ModelChoiceField(label="dictionary name", queryset=dictionary.objects.all())
