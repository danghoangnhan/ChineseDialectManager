from collections import OrderedDict, defaultdict

import pandas as pd
from django.db.models.signals import post_save
from django.dispatch import receiver
from import_export import resources, fields
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
        mapping = defaultdict(lambda: defaultdict(dict))
        dictionary_name_list = list(self.dictionary_list.values_list('name', flat=True))
        values_list = list(vocabulary.objects.filter(dictionary_name__in=dictionary_name_list).values())
        headers = []
        for data_element in values_list:
            mapping[data_element['symbol_text']][header['symbol_text']] = data_element['symbol_text']

            mapping[data_element['symbol_text']][data_element['dictionary_name'] + "_" + header["word"]] = data_element[
                "word"]

            mapping[data_element['symbol_text']][data_element['dictionary_name'] + "_" + header["tone"]] = data_element[
                "tone"]

            mapping[data_element['symbol_text']][data_element['dictionary_name'] + "_" + header["ipa"]] = data_element[
                "ipa"]

        df = pd.DataFrame.from_dict(mapping, orient='index')
        df.dropna(axis=0, how='any', inplace=True)  # Drop rows with NaN values
        data.wipe()
        for column in df.columns:
            if column.endswith(header["tone"]):
                converted_column = [convert_tone(
                    tone_original=int(float(element)),
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
        # no-op if this is the 'confirm' step
        return
    else:
        # your custom logic here
        # this will be executed only on the 'import' step
        pass
