from django import forms
from import_export.forms import ImportForm, ConfirmImportForm

from dictionaries.models import dictionary

tone_convert_type = [("BC_AT", "BC TO AT"), ("AT_BC", "AT TO BC")]
enable_tone_option = [("1", "yes"), ("2", "no")]


class VocabularyImportForm(ImportForm):
    dictionary_name = forms.ModelChoiceField(label="dictionary_name", queryset=dictionary.objects.all(), required=True)


class VocabularyConfirmImportForm(ConfirmImportForm):
    dictionary_name = forms.ModelChoiceField(label="dictionary_name", queryset=dictionary.objects.all(), required=True)


class NoteOptionForm(forms.Form):
    enable_tone_option = forms.ChoiceField(widget=forms.Select, choices=tone_convert_type)
    tone_convert_choice_form = forms.ChoiceField(widget=forms.RadioSelect, choices=tone_convert_type)
