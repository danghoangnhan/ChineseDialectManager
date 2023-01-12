from import_export import resources, fields

from dictionaries.models import dictionary
from rules.models import rules


class RulesResource(resources.ModelResource):
    id = fields.Field(column_name=id)
    name = fields.Field(column_name='name', attribute='name')
    unicode_repr = fields.Field(column_name='unicode_repr', attribute='unicode_repr')
    descriptors = fields.Field(column_name='descriptors', attribute='descriptor')
    type = fields.Field(column_name='type', attribute='type')
    dictionary = fields.Field(attribute='dictionary')

    def __init__(self, dictionary_name=None):
        super().__init__()
        if dictionary_name is not None:
            self.dictionary: dictionary = dictionary.objects.filter(id=int(dictionary_name)).first()

    class Meta:
        model = rules
        exclude = ('id')
        import_id_fields = ['name', 'unicode_repr', 'descriptors', 'type', 'dictionary']

    def before_import_row(self, row, **kwargs):
        row['dictionary'] = self.dictionary.name
