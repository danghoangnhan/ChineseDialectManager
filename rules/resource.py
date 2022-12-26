from import_export import resources, fields

from consonant import dict
from rules.models import rules


class RulesResource(resources.ModelResource):
    word = fields.Field(column_name='音', attribute='word')
    symbol_text = fields.Field(column_name='字', attribute='symbol_text')
    tone = fields.Field(column_name='聲調', attribute='tone')
    dictionary_name = fields.Field(attribute='dictionary_name')
    ipa = fields.Field(attribute='ipa')

    def __init__(self, dictionary_name=None):
        super()
        self.dictionary_name = dictionary_name

    class Meta:
        model = rules
        exclude = ('id', 'symbol_image', "ipa", "description")
        import_id_fields = ['word', 'symbol_text', 'tone', 'dictionary_name']

    def before_import_row(self, row, **kwargs):
        dictionaryObject = rules.objects.filter(id=int(self.dictionary_name)).first()
        row['dictionary_name'] = dictionaryObject.name
        row['ipa'] = dict.chaoshan2IPA(row['音'])
