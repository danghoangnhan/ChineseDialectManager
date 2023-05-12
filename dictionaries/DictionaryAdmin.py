from django.contrib import admin

from dictionaries.models import dictionary


@admin.register(dictionary)
class DictionaryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'input_tone', 'output_tone')
    list_editable = ('input_tone', 'output_tone')
    # change_list_template = "..dictionaries/dictionary/change_list.html"

    class Media:
        js = ('../static/dictionary/dictionary_admin.js',)  # Path to your JavaScript file

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = super().get_readonly_fields(request, obj)
        if obj and not obj.enable_tone_convert:
            readonly_fields += ('convert_type',)
        return readonly_fields

    def changeform_view(self, request, *args, **kwargs):
        self.readonly_fields = list(self.readonly_fields)
        usergroup = request.user.groups.filter(name__in=['author']).exists()
        if not usergroup:
            self.readonly_fields.append('price_upgrade')

        return super(DictionaryAdmin, self).changeform_view(request, *args, **kwargs)