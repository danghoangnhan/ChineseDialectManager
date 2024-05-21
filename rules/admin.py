from django.contrib.auth.admin import admin
from django_admin_row_actions import AdminRowActionsMixin
from django_object_actions import DjangoObjectActions
from import_export.admin import ExportActionMixin, ImportExportMixin, ImportExportActionModelAdmin

from rules.form import ToneImportForm, ToneConfirmImportForm
from rules.models import rules
from rules.resource import RulesResource


class RulesInline(admin.StackedInline):
    model = rules


@admin.register(rules)
class RulesAdmin(DjangoObjectActions,
                 AdminRowActionsMixin,
                 ImportExportMixin,
                 ImportExportActionModelAdmin,
                 ExportActionMixin,
                 admin.ModelAdmin):
    list_display = ('name', 'descriptors', 'unicode_repr', 'dictionary_name', 'type')
    list_filter = ("dictionary_name", 'type')
    search_fields = ('name', 'descriptors', 'unicode_repr', 'dictionary_name', 'type')

    resource_class = RulesResource
    import_form_class = ToneImportForm
    confirm_form_class = ToneConfirmImportForm
    list_per_page = 15
    cache = {'dictionary_name': None}

    def get_resource_kwargs(self, request, *args, **kwargs):
        rk = super().get_resource_kwargs(request, *args, **kwargs)
        if 'dictionary_name' in request.POST:
            self.cache['dictionary_name'] = request.POST.get('dictionary_name')
        rk['dictionary_name'] = self.cache['dictionary_name']
        return rk


admin.register(rules, RulesAdmin)
