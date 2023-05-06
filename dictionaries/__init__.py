from django.forms import forms


class CsvImportForm(forms.Form):
    csv_upload = forms.FileField()
