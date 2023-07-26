import pandas as pd
from django.db.models.signals import post_save
from django.dispatch import receiver
from import_export import resources, fields
from import_export.admin import ImportMixin

from consonant import Dictionary as DictConvert
from dictionaries.VocabularyModel import vocabulary
from dictionaries.models import dictionary
from rules.models import rules, tone_encode_mapper, tone_decode_mapper, convert_tone


class VocabularyAdminResource(ImportMixin, resources.ModelResource):
    word = fields.Field(column_name='音', attribute='word')
    symbol_text = fields.Field(column_name='字', attribute='symbol_text')
    tone = fields.Field(column_name='聲調', attribute='tone')
    dictionary_name = fields.Field(column_name='dictionary_name', attribute='dictionary_name')
    ipa = fields.Field(column_name='ipa', attribute='ipa')

    def __init__(self, dictionary_name=None, tone_option=None):
        super().__init__()
        self.tone_decoder = {}
        self.tone_encoder = {}
        self.dictionary = None
        self.dictconvert = None

        self.tone_decoder = tone_decode_mapper("A_T")
        if dictionary_name is not None:
            self.dictionary: dictionary = dictionary.objects.filter(id=int(dictionary_name)).first()
            ruleList = [rule for rule in rules.objects.filter(dictionary_name__exact=self.dictionary.name)]
            self.dictconvert = DictConvert(ruleList)

        if tone_option is not None:
            self.tone_encoder = tone_encode_mapper(str(tone_option))

    class Meta:
        model = vocabulary
        use_bulk = True
        batch_size = 10000

        store_row_values = True

    def before_import(self, dataset, using_transactions, dry_run, **kwargs):
        df = pd.DataFrame(dataset.dict)
        # Remove rows with None values
        df = df.dropna()
        # Convert 'symbol_text' column to lowercase
        df['音'] = df['音'].str.lower()

        # Assuming dataset is a pandas DataFrame
        df['字'] = df['字'].astype(str)

        if self.tone_encoder is not None:
            df['聲調'] = df['聲調'].apply(
                lambda x: convert_tone(tone_original=x, tone_decoder=self.tone_decoder, tone_encoder=self.tone_encoder)
            )

        if self.dictionary is not None:
            df['dictionary_name'] = self.dictionary.name

        if self.dictconvert is not None:
            df['ipa'] = df['音'].apply(self.dictconvert.chaoshan2IPA)

        # Remove duplicate rows
        df.drop_duplicates(inplace=True)
        # Check for duplicate rows
        dataset.wipe()
        headers = []
        for column in df.columns:
            headers.append(column)
            dataset.append_col(col=df[column].tolist(), header=column)
        dataset.headers = headers
        return dataset

    def before_save_instance(self, instance, using_transactions, dry_run):
        # during 'confirm' step, dry_run is True
        instance.dry_run = dry_run

    def get_resource_queryset(self):
        # Customize the queryset based on your requirements
        queryset = vocabulary.objects.filter(name__icontains='example')
        return queryset

    def after_export(self, queryset, data, *args, **kwargs):
        print(data)


@receiver(post_save, sender=vocabulary)
def my_callback(sender, **kwargs):
    instance = kwargs["instance"]
    if getattr(instance, "dry_run"):
        # no-op if this is the 'confirm' step
        return
    else:
        # your custom logic here
        # this will be executed only on the 'import' step
        pass
# def before_save_instance(self, instance, using_transactions, dry_run):
#     print(type(instance))
#     instance.symbol_text = str(instance.symbol_text)
#     instance.word = str(instance.word).lower()
#     instance.ipa = self.dictconvert.chaoshan2IPA(instance.word)
#     instance.dictionary_name = str(self.dictionary.name)

# def before_import_row(self, row, row_number=None, **kwargs):
#     row['dictionary_name'] = self.dictionary.name
#     row['字'] = str(row['字'])
#     row['音'] = str(row['音']).lower()
#     row['ipa'] = self.dictconvert.chaoshan2IPA(row['音'])
#     row['聲調'] = self.convert_tone(int(row['聲調']))

# def before_save_instance(instance, using_transactions, dry_run):
#     row['dictionary_name'] = self.dictionary.name
#     row['字'] = str(row['字'])
#     row['音'] = str(row['音']).lower()
#     row['ipa'] = self.dictconvert.chaoshan2IPA(row['音'])
#     row['聲調'] = self.convert_tone(int(row['聲調']))
#     instance.dry_run = dry_run
