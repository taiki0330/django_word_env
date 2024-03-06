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



def generate_report(request, pk):
    crime = Crime.objects.get(pk=pk)
    doc = DocxTemplate("/Users/matsuzakidaiki/anaconda3/envs/django_word_env/wordproject/docx_templates/犯罪事実.docx")
    context = {'title': crime.title, 'detail': crime.detail, 'division': crime.division.name}
    doc.render(context)

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
    response['Content-Disposition'] = 'attachment; filename="report.docx"'
    doc.save(response)

    return response