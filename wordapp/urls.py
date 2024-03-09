from django.urls import path
from .views import DivisionListView, CrimeListview, CrimeDetailView, CrimeCreate, CrimeDelete, CrimeUpdate, select_template

urlpatterns = [
    path('', DivisionListView.as_view(), name='division_list'),
    path('crime_list/<int:division_id>', CrimeListview.as_view(), name='crime_list'),
    path('crime_list/<int:division_id>/create/', CrimeCreate.as_view(), name="crime_create"),
    path('crime/<int:pk>', CrimeDetailView.as_view(), name='crime_detail'),
    path('crime/delete/<int:pk>/', CrimeDelete.as_view(), name='crime_delete'),
    path('crime/update/<int:pk>/', CrimeUpdate.as_view(), name='crime_update'),
    path('report/<int:pk>', select_template, name='select_template'),
]
