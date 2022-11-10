from django.contrib import admin
from django.urls import path
from apps.dictionary.views import DictionaryFilterView, download_csv

urlpatterns = [
    path('admin/', admin.site.urls, name='index'),

    path('', DictionaryFilterView.as_view(), name='index'),
    path('download/', download_csv, name='download_csv'),
]
