from django.contrib import admin
from django.urls import path

from apps.dictionary.views import home_view, export_data, import_data

urlpatterns = [
    path('admin/', admin.site.urls, name='index'),
    path('', home_view, name="index"),
    path('export/', export_data, name="export"),
    path('import/', import_data, name="import")
]