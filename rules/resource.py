from import_export import resources, fields
from dictionaries.models import dictionary
from rules.models import rules


class RulesResource(resources.ModelResource):
    name = fields.Field(column_name='name', attribute='name')
    unicode_repr = fields.Field(column_name='unicode_repr', attribute='unicode_repr')
    descriptors = fields.Field(column_name='descriptors', attribute='descriptors')
    type = fields.Field(column_name='type', attribute='type')
    dictionary_name = fields.Field(attribute='dictionary_name')

    def __init__(self, dictionary_name=None):
        super().__init__()
        if dictionary_name is not None:
            self.dictionary: dictionary = dictionary.objects.filter(id=int(dictionary_name)).first()

    class Meta:
        model = rules
        use_bulk = True
        batch_size = 1000
        skip_unchanged = True
        report_skipped = True
        raise_errors = False
        import_id_fields = ['name', 'unicode_repr', 'type', 'descriptors']

    def before_import_row(self, row, row_number=None, **kwargs):
        row['dictionary_name'] = self.dictionary.name
