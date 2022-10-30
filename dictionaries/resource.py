from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget

from dictionaries.models import dictionary


class VocabularyAdminResource(resources.ModelResource):
    word = fields.Field(column_name='word', attribute='word')

    class Meta:
        model = dictionary
        fields = (
            'word',
            'symbol_text',
            'symbol_image',
            'tone',
        )
        exclude = ('id',)
        import_id_fields = ('symbol_text', 'word', 'tone',)
