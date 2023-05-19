from import_export import resources, fields
from import_export.admin import ImportMixin

from consonant import Dictionary as DictConvert
from dictionaries.VocabularyModel import vocabulary
from dictionaries.models import dictionary
from rules.models import rules


class VocabularyAdminResource(ImportMixin, resources.ModelResource):
    report_error_column = False  # a parameter to report table column not defined in the resource class
    word = fields.Field(column_name='音', attribute='word')
    symbol_text = fields.Field(column_name='字', attribute='symbol_text')
    tone = fields.Field(column_name='聲調', attribute='tone')
    dictionary_name = fields.Field(column_name='dictionary_name', attribute='dictionary_name')
    ipa = fields.Field(column_name='ipa', attribute='ipa')

    def __init__(self, dictionary_name=None):
        super().__init__()
        if dictionary_name is not None:
            self.dictionary: dictionary = dictionary.objects.filter(id=int(dictionary_name)).first()
            ruleList = [rule for rule in rules.objects.filter(dictionary_name__exact=self.dictionary.name)]
            self.dictconvert = DictConvert(ruleList)

    class Meta:
        model = vocabulary
        # use_bulk = True
        # batch_size = 10000
        exclude = ('id')
        import_id_fields = ['word', 'symbol_text', 'tone', 'dictionary_name']
        # store_row_values = True
        # # skip_html_diff = True
        # use_transactions = True
        # force_init_instance = False

    # def before_import(self, dataset, using_transactions, dry_run, **kwargs):
    #     word_list = [str(element) for element in dataset['字']]
    #     symbol_text_list = [str(element).lower() for element in dataset['音']]
    #     ipa_list = [self.dictconvert.chaoshan2IPA(element) for element in symbol_text_list]
    #     dictionary_list = ([str(self.dictionary.name) for _ in word_list])
    #
    #     del dataset['字']
    #     del dataset['音']
    #     dataset.insert_col(
    #         0, col=word_list, header="字"
    #     )
    #     dataset.insert_col(
    #         1, col=symbol_text_list, header="音"
    #     )
    #     dataset.insert_col(
    #         2, col=dictionary_list, header="dictionary_name"
    #     )
    #     dataset.insert_col(
    #         3, col=dictionary_list, header="ipa"
    #     )
    #     return dataset

    # def before_save_instance(self, instance, using_transactions, dry_run):
    #     print(type(instance))
    #     instance.symbol_text = str(instance.symbol_text)
    #     instance.word = str(instance.word).lower()
    #     instance.ipa = self.dictconvert.chaoshan2IPA(instance.word)
    #     instance.dictionary_name = str(self.dictionary.name)
    def before_import_row(self, row, **kwargs):
        row['dictionary_name'] = self.dictionary.name
        row['音'] = str(row['音']).lower()
        row['ipa'] = self.dictconvert.chaoshan2IPA(row['音'])

