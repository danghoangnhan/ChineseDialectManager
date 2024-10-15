from django import forms
from import_export.forms import ImportForm, ConfirmImportForm
from dictionary.models import dictionary
from rules.models import rules


class ToneImportForm(ImportForm):
    dictionary_name = forms.ModelChoiceField(label="dictionary_name", queryset=dictionary.objects.all(), required=True)


class ToneConfirmImportForm(ConfirmImportForm):
    dictionary_name = forms.ModelChoiceField(label="dictionary_name", queryset=dictionary.objects.all(), required=True)


class RulesForm(forms.ModelForm):
    TYPE_CHOICES = [
        ('consonant', 'Consonant'),
        ('vowel', 'Vowel'),
    ]

    dictionary_name = forms.ModelChoiceField(
        queryset=dictionary.objects.all(),
        empty_label=None,
        to_field_name="name",
        widget=forms.Select(attrs={'class': 'vTextField'})
    )

    type = forms.ChoiceField(
        choices=TYPE_CHOICES,
        widget=forms.Select(attrs={'class': 'vTextField'})
    )

    class Meta:
        model = rules
        fields = ['name', 'unicode_repr', 'descriptors', 'dictionary_name', 'type']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'vTextField', 'style': 'width: 300px;'}),
            'unicode_repr': forms.TextInput(attrs={'class': 'vTextField'}),
            'descriptors': forms.TextInput(attrs={'class': 'vTextField'}),
            'type': forms.TextInput(attrs={'class': 'vTextField'}),
        }
