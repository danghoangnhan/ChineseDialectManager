from import_export import resources
from apps.dictionary.models import Dictionary


class DictionaryResource(resources.ModelResource):
    class Meta:
        model = Dictionary
