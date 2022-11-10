from django.urls import path

from apps.dictionary import views


urlpatterns = [
    path('/', views.DictionaryFilterView.as_view()),
    path('download/', views.download_csv, name='download_csv'),
]