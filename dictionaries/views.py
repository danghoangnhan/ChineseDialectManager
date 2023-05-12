from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse
from rest_framework.authtoken import admin

from dictionaries.VocabularyModel import vocabulary

from dictionaries.VocabularyAdmin import VocabularyAdmin


@staff_member_required
def my_admin_method_view(request):
    # Call the admin method
    my_model_admin = VocabularyAdmin(vocabulary, admin.site)
    response = my_model_admin.my_admin_method(request)
    return HttpResponse(response)