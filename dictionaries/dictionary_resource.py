from collections import OrderedDict
from django.db.models import Q, F
import tablib
from import_export import resources, fields
from import_export.admin import ImportMixin

from dictionaries.VocabularyModel import vocabulary
from dictionaries.models import dictionary
from rules.models import tone_decode_mapper, tone_encode_mapper

header = {
    'symbol_text': '字',
    'word': '音',
    'tone': '聲調',
    'ipa': 'IPA'
}


class DictionaryAdminResource(ImportMixin, resources.ModelResource):
    sql_query = """
       SELECT v1.symbol_text, v1.word, v1.ipa, v1.tone, v2.word, v2.ipa, v2.tone
       FROM vocabulary AS v1
       LEFT JOIN vocabulary AS v2 ON v1.symbol_text = v2.symbol_text
       WHERE v1.dictionary_name = '潮汕(2015)' AND v2.dictionary_name = '潮汕(1883)'
       """
    fields = OrderedDict()

    def __init__(self, tone_option=None, file_format=None, checkbox_field=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tone_decoder = {}
        self.tone_encoder = tone_encode_mapper("A_T")
        if tone_option is not None:
            self.tone_encoder = tone_decode_mapper(str(tone_option))
        if file_format is not None:
            self.file_format = file_format
        if checkbox_field is not None:
            self.dictionary_list = dictionary.objects.filter(id__in=checkbox_field)
            self.fields = OrderedDict()
            self.fields["v1.symbol_text"] = fields.Field(column_name=header["symbol_text"], attribute="v1.symbol_text")
            join_conditions = Q()
            select_columns = []
            join_statements = []
            where_conditions = Q()

            for i, element in enumerate(self.dictionary_list):
                queryset_word: str = "v{index}.{field}".format(index=i + 1, field="word")
                header_word: str = element.name + "_" + header["word"]
                queryset_tone: str = "v{index}.{field}".format(index=i + 1, field="tone")
                header_tone: str = element.name + "_" + header["tone"]
                queryset_ipa: str = "v{index}.{field}".format(index=i + 1, field="ipa")
                header_ipa: str = element.name + "_" + header["ipa"]
                select_columns.append(queryset_word)
                select_columns.append(queryset_tone)
                select_columns.append(queryset_ipa)

                self.fields[queryset_word] = fields.Field(column_name=header_word, attribute=queryset_word)
                self.fields[queryset_tone] = fields.Field(column_name=header_tone, attribute=queryset_tone)
                self.fields[queryset_ipa] = fields.Field(column_name=header_ipa, attribute=queryset_ipa)

                # Use Q object to construct the join condition
                join_condition = Q(**{f"v{i + 1}__symbol_text": F("v1__symbol_text")})
                where_condition = Q(dictionary_name=element.name)
                if i + 1 > 1:
                    join_statements.append(
                        "LEFT JOIN vocabulary AS v{index} ON v1.symbol_text = v{index}.symbol_text".format(index=i + 1)
                    )
                    join_conditions &= Q(**{f"v{i + 1}__symbol_text": F("v1__symbol_text")})
                where_conditions &= where_condition
            # Construct the SQL query
            self.sql_query = """
               SELECT v1.symbol_text, {select_columns}
               FROM vocabulary AS v1
               {join_statements}
               WHERE {where_conditions}
            """.format(
                select_columns=", ".join(select_columns),
                join_statements=" ".join(join_statements),
                where_conditions=" AND ".join(where_conditions),
            )

            print(join_statements)
            self.queryset = vocabulary.objects.filter(*where_conditions)
            print(self.queryset)

    def get_queryset(self):
        queryset = vocabulary.objects.extra(where=[], tables=["vocabulary"], where_select=[self.sql_query])
        return queryset
