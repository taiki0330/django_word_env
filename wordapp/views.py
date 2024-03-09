from django.views.generic import ListView, DetailView
from .models import Division, Crime
from django.shortcuts import render, redirect
from docxtpl import DocxTemplate
from django.http import HttpResponse
import os
import glob
from django.conf import settings
from wordproject.settings import BASE_DIR


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
#     doc = DocxTemplate("/Users/matsuzakidaiki/anaconda3/envs/django_word_env/wordproject/docx_templates/人着の写真撮影報告書.docx")
#     context = {
#         'division': crime.division.name,
#         'crime_name': crime.crime_name, 
#         'crime_fact': crime.crime_fact, 
#         'crime_start_date': crime.crime_start_date,
#         'crime_start_time': crime.crime_start_time,
#         'crime_end_date': crime.crime_end_date,
#         'crime_end_time': crime.crime_end_time,
#         'crime_place': crime.crime_place,
#         'suspect_honseki': crime.suspect_honseki,
#         'suspect_address': crime.suspect_address,
#         'suspect_job': crime.suspect_job,
#         'suspect_name': crime.suspect_name,
#         'suspect_birthday': crime.suspect_birthday,
#         }
#     doc.render(context)

#     response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
#     response['Content-Disposition'] = 'attachment; filename="report.docx"'
#     doc.save(response)

#     return response

# def select_template(request, pk):
#     crime = Crime.objects.get(pk=pk)
#     template_dir = settings.DOCX_TEMPLATE_DIR # docx_templatesディレクトリの絶対パスを取得
#     template_files = glob.glob(os.path.join(template_dir, '*.docx')) # .docx拡張子のファイルをすべて取得
#     # テンプレートファイル名のみをリストに格納する
#     templates = [os.path.basename(template_file) for template_file in template_files]
#     print(template_dir)
#     print("Templates found:", templates)  # 正しい変数名を使用する


#     if request.method == 'POST':
#         selected_template = request.POST.get('template')
#         template_path = os.path.join(template_dir, selected_template)
        
#         if os.path.exists(template_path) and os.path.isfile(template_path):
#             doc = DocxTemplate(template_path)
#             context = {'title': crime.title, 'detail': crime.detail}
#             doc.render(context)

#             response = HttpResponse(
#                 content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
#             )
#             response['Content-Disposition'] = 'attachment; filename="{}"'.format(selected_template)
#             doc.save(response)

#             return response

#     # テンプレートファイル名のみをリストに格納する
#     templates = [os.path.basename(template_file) for template_file in template_files]
#     return render(request, 'crime_detail.html', {'templates': templates, 'crime': crime, 'template_dir': template_dir, 'template_files': template_files})

def select_template(request, pk):
    crime = Crime.objects.get(pk=pk)

    # docx_templatesフォルダ内の全てのdocxファイルを取得
    template_folder = os.path.join(BASE_DIR, 'docx_templates')
    template_files = [file for file in os.listdir(template_folder) if file.endswith('.docx')]
    print(template_files)

    context = {
        'division': crime.division.name,
        'crime_name': crime.crime_name, 
        'crime_fact': crime.crime_fact, 
        'crime_start_date': crime.crime_start_date,
        'crime_start_time': crime.crime_start_time,
        'crime_end_date': crime.crime_end_date,
        'crime_end_time': crime.crime_end_time,
        'crime_place': crime.crime_place,
        'suspect_honseki': crime.suspect_honseki,
        'suspect_address': crime.suspect_address,
        'suspect_job': crime.suspect_job,
        'suspect_name': crime.suspect_name,
        'suspect_birthday': crime.suspect_birthday,
        'template_files': template_files,  # テンプレートファイルのリストを追加
    }

    doc = DocxTemplate(os.path.join(template_folder, template_files[0]))  # 最初のテンプレートを使用
    doc.render(context)

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
    response['Content-Disposition'] = 'attachment; filename="report.docx"'
    doc.save(response)

    return response