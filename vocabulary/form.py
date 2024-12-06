from django import forms
from import_export.forms import ConfirmImportForm, ExportForm, ImportForm

from dictionary.form import tone_convert_type
from dictionary.models import dictionary
from vocabulary.model import vocabulary


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


class VocabularyForm(forms.ModelForm):
    dictionary_name = forms.ModelChoiceField(
        queryset=dictionary.objects.all(),
        empty_label=None,
        to_field_name="name",
        widget=forms.Select(attrs={'class': 'vTextField'})
    )

    class Meta:
        model = vocabulary
        fields = ['word', 'tone', 'symbol_text', 'dictionary_name', 'ipa', 'description']
        widgets = {
            'word': forms.TextInput(attrs={'class': 'vTextField', 'style': 'width: 300px;'}),
            'tone': forms.TextInput(attrs={'class': 'vTextField'}),
            'symbol_text': forms.TextInput(attrs={'class': 'vTextField'}),
            'ipa': forms.TextInput(attrs={'class': 'vTextField'}),
            'description': forms.Textarea(
                attrs={'class': 'vLargeTextField', 'rows': 4, 'cols': 40, 'style': 'width: 500px;'}),
        }