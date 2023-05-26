from import_export import resources
from import_export.admin import ImportMixin

from dictionaries.VocabularyModel import vocabulary
from dictionaries.models import dictionary
from rules.models import tone_decode_mapper, tone_encode_mapper


class DictionaryAdminResource(ImportMixin, resources.ModelResource):

    def __init__(self, tone_option=None):
        super().__init__()
        self.tone_decoder = {}
        self.tone_encoder = {}
        self.tone_decoder = tone_decode_mapper("A_T")
        if tone_option is not None:
            self.tone_encoder = tone_encode_mapper(str(tone_option))

    class Meta:
        model = dictionary
        # use_bulk = True
        # batch_size = 10000
        exclude = ('id')
        import_id_fields = ['word', 'symbol_text', 'tone', 'dictionary_name']
        # store_row_values = True
        # # skip_html_diff = True
        # use_transactions = True
        # force_init_instance = False

    def before_import(self, dataset, using_transactions, dry_run, **kwargs):
        word_list = [str(element) for element in dataset['字']]
        symbol_text_list = [str(element).lower() for element in dataset['音']]

        if self.dictconvert is not None:
            ipa_list = [self.dictconvert.chaoshan2IPA(element) for element in symbol_text_list]
            dataset.insert_col(4, col=ipa_list, header="ipa")

        if self.tone_encoder is not None:
            tone_list = ([self.convert_tone(element) for element in dataset['聲調']])
            del dataset['聲調']
            dataset.insert_col(2, col=tone_list, header="聲調")

        del dataset['字']
        del dataset['音']
        dataset.insert_col(0, col=word_list, header="字")
        dataset.insert_col(1, col=symbol_text_list, header="音")
        return dataset

    # def before_save_instance(self, instance, using_transactions, dry_run):
    #     print(type(instance))
    #     instance.symbol_text = str(instance.symbol_text)
    #     instance.word = str(instance.word).lower()
    #     instance.ipa = self.dictconvert.chaoshan2IPA(instance.word)
    #     instance.dictionary_name = str(self.dictionary.name)

    # def before_import_row(self, row, row_number=None, **kwargs):
    #     row['dictionary_name'] = self.dictionary.name
    #     row['字'] = str(row['字'])
    #     row['音'] = str(row['音']).lower()
    #     row['ipa'] = self.dictconvert.chaoshan2IPA(row['音'])
    #     row['聲調'] = self.convert_tone(int(row['聲調']))

    # def before_save_instance(instance, using_transactions, dry_run):
    #     row['dictionary_name'] = self.dictionary.name
    #     row['字'] = str(row['字'])
    #     row['音'] = str(row['音']).lower()
    #     row['ipa'] = self.dictconvert.chaoshan2IPA(row['音'])
    #     row['聲調'] = self.convert_tone(int(row['聲調']))
    #     instance.dry_run = dry_run

    def convert_tone(self, tone_original):
        if tone_original in self.tone_encoder:
            key1, key2 = self.tone_encoder.get(tone_original)
            return self.tone_decoder.get((key1, key2), -1)
        return -1  # Return -1 if the encoded value is not found in the encode mapper
