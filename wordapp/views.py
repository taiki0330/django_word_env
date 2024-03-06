from django.views.generic import ListView, DetailView
from .models import Division, Crime
from django.shortcuts import render, redirect
from docxtpl import DocxTemplate
from django.http import HttpResponse

class DivisionListView(ListView):
    model = Division
    template_name = 'genre_list.html'

class CrimeListview(ListView):
    template_name = 'crime_list.html'
    
    def get_queryset(self):
        return Crime.objects.filter(division_id=self.kwargs['division_id'])



class CrimeDetailView(DetailView):
    model = Crime
    template_name = 'crime_detail.html'