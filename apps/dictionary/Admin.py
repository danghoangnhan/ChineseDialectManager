import csv

from django.forms import forms
from django.shortcuts import redirect, render
from django.urls import path
from import_export.admin import ImportExportModelAdmin
from django.contrib import admin
from apps.dictionary.models import Dictionary



class CsvImportForm(forms.Form):
    csv_file = forms.FileField()


class DictionaryAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    change_list_template = "entities/dictionaries_changelist.html"
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')
    fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]

    # def get_urls(self):
    #     urls = super().get_urls()
    #     my_urls = [
    #         path('import-csv/', self.import_csv),
    #     ]
    #     return my_urls + urls
    #
    # def import_csv(self, request):
    #     if request.method == "POST":
    #         csv_file = request.FILES["csv_file"]
    #         reader = csv.reader(csv_file)
    #         # Create Hero objects from passed in data
    #         # ...
    #         self.message_user(request, "Your csv file has been imported")
    #         return redirect("..")
    #     form = CsvImportForm()
    #     payload = {"form": form}
    #     return render(
    #         request, "admin/csv_form.html", payload
    #     )


DictionaryAdminSite = DictionaryAdmin()

