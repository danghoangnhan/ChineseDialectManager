from import_export import resources, fields

from consonant import Dictionary as DictConvert
from dictionaries.VocabularyModel import vocabulary
from dictionaries.models import dictionary
from rules.models import rules


class VocabularyAdminResource(resources.ModelResource):
    word = fields.Field(column_name='音', attribute='word')
    symbol_text = fields.Field(column_name='字', attribute='symbol_text')
    tone = fields.Field(column_name='聲調', attribute='tone')
    dictionary_name = fields.Field(attribute='dictionary_name')
    ipa = fields.Field(attribute='ipa')

    def __init__(self, dictionary_name=None):
        super().__init__()
        if dictionary_name is not None:
            self.dictionary: dictionary = dictionary.objects.filter(id=int(dictionary_name)).first()
            ruleList: list[rules] = [rule for rule in rules.objects.filter(dictionary__exact=self.dictionary.id)]
            self.dictconvert = DictConvert(ruleList)

    class Meta:
        model = vocabulary
        exclude = ('id', 'symbol_image', "ipa", "description")
        import_id_fields = ['word', 'symbol_text', 'tone', 'dictionary_name']

    def before_import_row(self, row, **kwargs):
        row['dictionary_name'] = self.dictionary.name
        row['ipa'] = self.dictconvert.chaoshan2IPA(row['音'])
        row['音'] = str(row['音']).lower()

