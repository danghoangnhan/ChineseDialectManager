import csv
from django.http import HttpResponse
from django_filters import FilterSet
from django_filters.views import FilterView

from apps.dictionary import models


def get_field_names(model_class):
    fields = model_class._meta.get_fields()
    field_names = [field.name for field in fields]
    return field_names


class DictionaryFilter(FilterSet):
    class Meta:
        model = models.Dictionary
        fields = ['Word', 'Tone']


class DictionaryFilterView(FilterView):
    filterset_class = DictionaryFilter
    paginate_by = 20
    template_name = './dictionary_filter.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['field_names'] = get_field_names(models.Dictionary)
        # Create a values object so it can be accessed by field_name
        context['page_obj_values'] = context['page_obj'].object_list.values()
        return context


def download_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="dictionary.csv"'

    field_names = get_field_names(models.Dictionary)
    queryset = models.Dictionary.objects.all().order_by('word', 'tone').values(*field_names)
    filter_obj = DictionaryFilter(request.GET, queryset=queryset)

    writer = csv.writer(response)
    writer.writerow(field_names)
    for row in filter_obj.qs:
        row_data = [row[field_name] for field_name in field_names]
        writer.writerow(row_data)

    return response
