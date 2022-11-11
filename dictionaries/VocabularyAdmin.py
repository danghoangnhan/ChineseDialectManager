import csv
from django import forms as form_2
from django.contrib.auth.admin import admin
from django.core.checks import messages
from django.forms import forms
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.urls import path, reverse
from django_admin_row_actions import AdminRowActionsMixin
from django_object_actions import DjangoObjectActions
from import_export.admin import ExportActionMixin, ImportMixin, ImportExportMixin, ImportExportActionModelAdmin
from import_export.forms import ImportForm, ConfirmImportForm

from consonant import Dictionary
from dictionaries import CsvImportForm
from dictionaries.VocabularyModel import vocabulary
from dictionaries.models import dictionary
from dictionaries.resource import VocabularyAdminResource

chaoshan = Dictionary()


class VocabularyInline(admin.StackedInline):
    model = vocabulary


class CustomImportForm(ImportForm):
    author = form_2.ModelChoiceField(
        queryset=dictionary.objects.all(),
        required=True)


class CustomConfirmImportForm(ConfirmImportForm):
    dictionary_name = form_2.ModelChoiceField(
        queryset=dictionary.objects.all(),
        required=True)


@admin.register(vocabulary)
class VocabularyAdmin(DjangoObjectActions,
                      AdminRowActionsMixin,
                      ImportExportMixin,
                      ImportExportActionModelAdmin,
                      ExportActionMixin,
                      admin.ModelAdmin):
    list_display = ('symbol_text', 'word', 'tone', 'ipa', 'description', 'dictionary_name')
    list_filter = ("dictionary_name", )
    search_fields = ("dictionary_name", )

    actions = ['update_ipa']
    change_list_template = "../templates/dictionaries/dictionary/change_list.html"
    resource_class = VocabularyAdminResource

    def get_urls(self):
        urls = super().get_urls()
        new_urls = [path('upload-csv/', self.upload_csv), ]
        return new_urls + urls

    @admin.action(description='Update the IPA')
    def update_ipa(self, request, obj):

        selected = request.POST.getlist(admin.ModelAdmin)

    def upload_csv(self, request):

        if request.method == "POST":
            csv_file = request.FILES["csv_upload"]

            if not csv_file.name.endswith('.csv'):
                messages.warning(request, 'The wrong file type was uploaded')
                return HttpResponseRedirect(request.path_info)

            file_data = csv_file.read().decode("utf-8").split("\n")
            objectList = [generateVocabulary(x) for x in file_data[1:]]
            bulk_msj = vocabulary.objects.bulk_create(objectList)
            url = reverse('admin:index')
            return HttpResponseRedirect(url)

        form = CsvImportForm()
        data = {"form": form}
        return render(request, "admin/csv_upload.html", data)


def generateVocabulary(data) -> vocabulary:
    fields = data.replace('\r', '').split(",")
    result = vocabulary(
        symbol_text=fields[0],
        word=str(fields[1]).lower(),
        tone=fields[2],
        ipa=chaoshan.chaoshan2IPA(str(fields[1]).lower()),
        description='',
        dictionary_name=dictionary.objects.get(name__contains='潮汕')
    )
    return result
