from django.urls import path
from .views import IndexView, DivisionListView, CrimeListview, CrimeDetailView, CrimeCreate, CrimeDelete, CrimeUpdate, generate_report,suggest_crime_name, CrimeWizardView
urlpatterns = [
    path('', IndexView.as_view(), name='home'),
    path('division_list', DivisionListView.as_view(), name='division_list'),
    path('crime_list/<int:division_id>', CrimeListview.as_view(), name='crime_list'),
    path('crime_list/<int:division_id>/create/', CrimeCreate.as_view(), name="crime_create"),
    path('crime_list/<int:division_id>/create/crime_wizard', CrimeWizardView.as_view(), name='crime_wizard'),
    path('crime/<int:pk>', CrimeDetailView.as_view(), name='crime_detail'),
    path('crime/delete/<int:pk>/', CrimeDelete.as_view(), name='crime_delete'),
    path('crime/update/<int:pk>/', CrimeUpdate.as_view(), name='crime_update'),
    path('report/<int:pk>', generate_report, name='generate_report'),
    path('api/suggest/crime/', suggest_crime_name, name='suggest_crime_name'),
]