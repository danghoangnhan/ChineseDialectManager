from django.contrib import admin
from django.core.checks import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import path, reverse

from dictionaries import CsvImportForm
from dictionaries.models import dictionary


@admin.register(dictionary)
class DictionaryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    change_list_template = "../templates/dictionaries/dictionary/change_list.html"

    def get_urls(self):
        urls = super().get_urls()
        new_urls = [path('upload-csv/', self.upload_csv), ]
        return new_urls + urls

    def upload_csv(self, request):

        if request.method == "POST":
            csv_file = request.FILES["csv_upload"]

            if not csv_file.name.endswith('.csv'):
                messages.warning(request, 'The wrong file type was uploaded')
                return HttpResponseRedirect(request.path_info)

            file_data = csv_file.read().decode("utf-8")
            csv_data = file_data.split("\n")

            for x in csv_data:
                fields = x.split(",")
                created = dictionary.objects.update_or_create(
                    name=fields[0],
                    description=fields[1],
                )
            url = reverse('admin:index')
            return HttpResponseRedirect(url)

        form = CsvImportForm()
        data = {"form": form}
        return render(request, "admin/csv_upload.html", data)
