from import_export import resources
from import_export.admin import ImportMixin

from dictionaries.models import dictionary
from rules.models import tone_decode_mapper, tone_encode_mapper


class DictionaryAdminResource(ImportMixin, resources.ModelResource):

    def __init__(self, tone_option=None, file_format=None, checkbox_field=None):
        super().__init__()
        self.tone_decoder = {}
        self.tone_encoder = tone_encode_mapper("A_T")
        if tone_option is not None:
            self.tone_encoder = tone_decode_mapper(str(tone_option))
        if file_format is not None:
            self.file_format = file_format
        if checkbox_field is not None:
            self.dictionary_list = checkbox_field

    class Meta:
        model = dictionary


