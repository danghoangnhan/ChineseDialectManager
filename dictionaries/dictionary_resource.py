import copy
from collections import OrderedDict, defaultdict

import pandas as pd
from django.db.models.signals import post_save
from django.dispatch import receiver
from import_export import resources
from import_export.admin import ImportMixin

from dictionaries.VocabularyModel import vocabulary
from dictionaries.models import dictionary
from rules.models import tone_decode_mapper, tone_encode_mapper, convert_tone

header = {
    'symbol_text': '字',
    'word': '音',
    'tone': '聲調',
    'ipa': 'IPA'
}


class DictionaryAdminResource(ImportMixin, resources.ModelResource):
    fields = OrderedDict()

    class Meta:
        model = vocabulary

    def __init__(self, tone_option=None, file_format=None, checkbox_field=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tone_decoder = {}
        self.tone_encoder = tone_encode_mapper("A_T")
        self.fields = OrderedDict()
        self.export_header = [header['symbol_text']]
        if tone_option is not None:
            self.tone_decoder = tone_decode_mapper(str(tone_option))
        if file_format is not None:
            self.file_format = file_format
        if checkbox_field is not None:
            self.dictionary_list = dictionary.objects.filter(id__in=checkbox_field)

    def after_export(self, queryset, data, *args, **kwargs):

        dictionary_name_list = list(self.dictionary_list.values_list('name', flat=True))
        values_list = list(vocabulary.objects.filter(dictionary_name__in=dictionary_name_list).values())
        headers = []
        mapping_result = dict()

        for data_element in values_list:
            if data_element['symbol_text'] not in mapping_result:
                mapping_result[data_element['symbol_text']] = dict()
            if data_element["dictionary_name"] not in mapping_result[data_element['symbol_text']]:
                mapping_result[data_element['symbol_text']][data_element["dictionary_name"]] = []
            mapping_result[data_element['symbol_text']][data_element["dictionary_name"]].append(data_element)

        mapper = dict()
        counter = 0
        for key, value in mapping_result.items():
            current_row = [{
                header['symbol_text']: key
            }]
            for dictionary_value in dictionary_name_list:
                if dictionary_value not in value:
                    emptyObject = dict()
                    emptyObject["word"] = ''
                    emptyObject["tone"] = ''
                    emptyObject["ipa"] = ''
                    value.setdefault(dictionary_value, [emptyObject])

                get_dictionary_item_list = value[dictionary_value]
                result = []
                for dictionary_item in get_dictionary_item_list:
                    clone_props = copy.deepcopy(current_row)
                    for item in clone_props:
                        item[dictionary_value + "_" + header["word"]] = dictionary_item["word"]
                        item[dictionary_value + "_" + header["tone"]] = dictionary_item["tone"]
                        item[dictionary_value + "_" + header["ipa"]] = dictionary_item["ipa"]
                        result.append(item)
                current_row = result
            for row in current_row:
                mapper[counter] = row
                counter += 1
        df = pd.DataFrame.from_dict(mapper, orient='index')
        data.wipe()
        for column in df.columns:
            if column.endswith(header["tone"]):
                converted_column = [convert_tone(
                    tone_original=numerical(element),  # Convert string to float, then round to int
                    tone_decoder=self.tone_decoder,
                    tone_encoder=self.tone_encoder)
                    for element in df[column].tolist()]
                data.append_col(col=converted_column, header=column)
            else:
                data.append_col(col=df[column].tolist(), header=column)
            headers.append(column)
        data.headers = headers
        return data


@receiver(post_save, sender=vocabulary)
def my_callback(sender, **kwargs):
    instance = kwargs["instance"]
    if getattr(instance, "dry_run"):
        return
    else:
        pass


def numerical(value):
    try:
        result = int(float(value))
        return result
    except ValueError:
        return -1
