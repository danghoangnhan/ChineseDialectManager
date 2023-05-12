import csv
from collections import defaultdict
from django import forms
from django import forms as form_2
from django.contrib.admin import helpers
from django.contrib.auth.admin import admin
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import path
from django_admin_row_actions import AdminRowActionsMixin
from django_object_actions import DjangoObjectActions
from import_export.admin import ExportActionMixin, ImportExportMixin, ImportExportActionModelAdmin
from import_export.forms import ImportForm, ConfirmImportForm

from dictionaries.VocabularyModel import vocabulary
from dictionaries.models import dictionary
from dictionaries.resource import VocabularyAdminResource
from dictionaries.form import NoteOptionForm

class VocabularyInline(admin.StackedInline):
    model = vocabulary


class CustomImportForm(ImportForm):
    dictionary_name = form_2.ModelChoiceField(
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
    search_fields = ("dictionary_name",)
    actions = ['export_as_csv']
    tone_option = None

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('update_tone_option/', self.update_tone_option, name="update_tone_option"),
        ]
        return my_urls + urls

    def update_tone_option(self, request):
        if request.method == 'POST':
            form_data = request.POST  # Get the form data
            test = request.FILES
            # Access individual form fields using their names
            rows = form_data.get('rows')
            file_field = request.FILES.get(
                'file_field_name')  # Replace 'file_field_name' with the actual name of the file input field

            # Process the form data as needed

            # Example: Print the form data
            print(rows)
            print(file_field)

            # Return an appropriate response
            return HttpResponse('Form submitted successfully')

            # Handle GET request or other cases
            # You can render the template with an empty context or any additional data needed
        return redirect(request.META.get('HTTP_REFERER'))

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['formData'].widget = forms.ClearableFileInput(attrs={'multiple': True})
        return form

    change_list_template = "../templates/dictionaries/vocabulary/change_list.html"
    resource_class = VocabularyAdminResource

    def changelist_view(self, request, extra_context=None):
        response = super(VocabularyAdmin, self).changelist_view(request, extra_context=extra_context, )
        if self.tone_option is None:
            self.tone_option = list(dictionary.objects.all())
            self.tone_option = [toneOption(diction) for diction in self.tone_option]
        map(lambda r: r.update({'check_box': helpers.checkbox.render(helpers.ACTION_CHECKBOX_NAME, r['pk'])}),
            self.tone_option)
        response.context_data['dictionary_tone_option'] = list(self.tone_option)
        response.context_data['note_form'] = NoteOptionForm


        return response

    @admin.action(description=' export to dictionary format csv')
    def export_as_csv(self, request, queryset):
        meta = vocabulary._meta
        header = ['字']
        template = ['音', '聲調', 'IPA']
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)
        v = defaultdict(dict)
        datalist = [obj for obj in queryset]
        dictionary_list = set([getattr(obj, 'dictionary_name') for obj in datalist])
        mapping = defaultdict(dict)
        for data_element in datalist:
            if mapping.get(data_element) is None:
                mapping[getattr(data_element, 'word')] = defaultdict()
            mapping[getattr(data_element, 'word')][getattr(data_element, 'dictionary_name')] = data_element

        for dictionary_name in dictionary_list:
            for col in template:
                header.append(dictionary_name + '_' + col)
        writer.writerow(header)
        for key in mapping:
            rowValue = [key]
            inode = mapping.get(key)
            for dictionary_name in dictionary_list:
                obj = inode.get(dictionary_name)
                if obj is not None:
                    rowValue.append(getattr(obj, 'word'))
                    rowValue.append(getattr(obj, 'tone'))
                    rowValue.append(getattr(obj, 'ipa'))
                else:
                    rowValue.append(None)
                    rowValue.append(None)
                    rowValue.append(None)
            writer.writerow(rowValue)
        return response


class toneOption():
    def __init__(self, dictionary):
        self.dictionary = dictionary
        self.enable_tone_convert: False = False
        self.convert: str = ''
