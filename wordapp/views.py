from django.views.generic import ListView, DetailView
from .models import Division, Crime
from django.shortcuts import render, redirect
from docxtpl import DocxTemplate
from django.http import HttpResponse
import os


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



# def generate_report(request, pk):
#     crime = Crime.objects.get(pk=pk)
#     doc = DocxTemplate("/Users/matsuzakidaiki/anaconda3/envs/django_word_env/wordproject/docx_templates/現場の写真撮影報告書.docx")
#     context = {'title': crime.title, 'detail': crime.detail, 'division': crime.division.name}
#     doc.render(context)

#     response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
#     response['Content-Disposition'] = 'attachment; filename="report.docx"'
#     doc.save(response)

#     return response

def select_template(request, pk):
    crime = Crime.objects.get(pk=pk)
    template_dir = '/Users/matsuzakidaiki/anaconda3/envs/django_word_env/wordproject/docx_templates'
    templates = os.listdir(template_dir)

    if request.method == 'POST':
        selected_template = request.POST.get('template')
        doc = DocxTemplate(template_dir + selected_template)
        context = {'title': crime.title, 'detail': crime.detail}
        doc.render(context)

        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
        response['Content-Disposition'] = f'attachment; filename="{selected_template}"'
        doc.save(response)

        return response
    else:
        return render(request, 'crime_detail.html', {'templates': templates, 'crime': crime})
    