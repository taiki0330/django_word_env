from django.urls import path
from .views import DivisionListView, CrimeListview, CrimeDetailView, select_template

urlpatterns = [
    path('', DivisionListView.as_view(), name='division_list'),
    path('crime_list/<int:division_id>', CrimeListview.as_view(), name='crime_list'),
    path('crime/<int:pk>', CrimeDetailView.as_view(), name='crime_detail'),
    path('report/<int:pk>', select_template, name='select_template'),
]
