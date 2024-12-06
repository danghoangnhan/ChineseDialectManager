from import_export import resources, fields
from dictionary.models import dictionary
from rules.models import rules
import pandas as pd


class RulesResource(resources.ModelResource):
    name = fields.Field(column_name='name', attribute='name')
    unicode_repr = fields.Field(column_name='unicode_repr', attribute='unicode_repr')
    descriptors = fields.Field(column_name='descriptors', attribute='descriptors')
    type = fields.Field(column_name='type', attribute='type')
    dictionary_name = fields.Field(column_name='dictionary_name', attribute='dictionary_name')

    def __init__(self, dictionary_name=None):
        super().__init__()
        self.dictionary = None
        if dictionary_name is not None:
            self.dictionary: dictionary = dictionary.objects.filter(id=int(dictionary_name)).first()

    class Meta:
        model = rules
        use_bulk = True
        batch_size = 1000
        skip_unchanged = True
        report_skipped = True
        # import_id_fields = ['name', 'unicode_repr', 'type', 'descriptors']

    def before_import(self, dataset, using_transactions, dry_run, **kwargs):
        df = pd.DataFrame(dataset.dict)
        if self.dictionary is not None:
            df['dictionary_name'] = self.dictionary.name
        # Remove duplicate rows
        df.drop_duplicates(inplace=True)
        dataset.wipe()
        headers = []
        for column in df.columns:
            headers.append(column)
            dataset.append_col(col=df[column].tolist(), header=column)
        dataset.headers = headers
        return dataset
