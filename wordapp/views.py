from django.views import View
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView, TemplateView
from django.utils.dateparse import parse_date
from .models import Division, Crime
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from formtools.wizard.views import SessionWizardView
from .forms import CrimeInfoForm, CrimeDetailForm, SuspectInfoForm
from django.core.exceptions import ValidationError
from docxtpl import DocxTemplate
from django.http import HttpResponse
from PIL import Image
import pytesseract
from django.core.files.storage import FileSystemStorage
import os
import glob
from django.conf import settings
from wordproject.settings import DOCX_TEMPLATE_DIR
from django.core.files.storage import default_storage
from django.utils.dateformat import DateFormat
from django.utils.formats import get_format
import datetime
from django.http import JsonResponse
import json
import markovify
from django.views.decorators.csrf import csrf_exempt
import openai
import io
# from pathlib import Path
from google.cloud import vision


class IndexView(TemplateView):
    template_name = "top.html"



class DivisionListView(ListView):
    model = Division
    template_name = 'genre_list.html'

class CrimeListview(ListView):
    template_name = 'crime_list.html'
    
    def get_queryset(self):
        return Crime.objects.filter(division_id=self.kwargs['division_id'])
    
    def get_context_data(self, **kwargs):
        # 親クラスの get_context_data を呼び出して、コンテキストを取得
        context = super().get_context_data(**kwargs)
        # コンテキストに division_id を追加
        context['division_id'] = self.kwargs.get('division_id')
        return context



class CrimeDetailView(DetailView):
    model = Crime
    template_name = 'crime_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        crime = self.get_object()
        # CrimeインスタンスからDivisionインスタンスのIDを取得
        context['division_id'] = crime.division.id
        return context


class CrimeCreate(CreateView):
    model = Crime
    fields = [
        'crime_name', 
        'crime_name_second', 
        'crime_start_date', 
        'crime_start_time', 
        'crime_end_date', 
        'crime_end_time', 
        'crime_place', 
        'crime_fact',
        'suspect_honseki',
        'suspect_address',
        'suspect_job',  
        'suspect_name',
        'suspect_birthday',
        ]
    template_name = 'crime_create.html'
    
    def form_valid(self, form):
        form.instance.division_id = self.kwargs['division_id']
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('crime_list', kwargs={'division_id': self.kwargs['division_id']})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['division_id'] = self.kwargs['division_id']
        return context



class CrimeWizardView(SessionWizardView):
    template_name = 'crime_wizard_form.html'
    form_list = [CrimeInfoForm, CrimeDetailForm, SuspectInfoForm]
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'django-word-env-ec1c972e15d9.json'
    

    def dispatch(self, request, *args, **kwargs):
        self.division_id = kwargs['division_id']
        request.session['division_id'] = self.division_id  # セッションにdivision_idを保存
        return super().dispatch(request, *args, **kwargs)
    
    def process_step(self, form):
        # ステップごとのフォームデータを取得してセッションに保存
        cleaned_data = form.cleaned_data
        step_data = {key: value if not isinstance(value, (datetime.date, datetime.time)) else str(value) for key, value in cleaned_data.items()}
        self.request.session[f'step_data_{self.steps.current}'] = step_data
        
        
        return self.get_form_step_data(form)
    
    def analyze_image(image_path):
        # 画像ファイルをGoogle Vision APIに送信し、解析結果を取得する
        client = vision.ImageAnnotatorClient()
        with io.open(image_path, 'rb') as image_file:
            content = image_file.read()

        image = vision.Image(content=content)
        response = client.text_detection(image=image)  # テキスト検出を使用
        texts = response.text_annotations
        return texts
    
    def get_template_names(self):
        # ステップ番号に基づいて異なるテンプレートを返す
        return [f'crime_wizard_form_step_{self.steps.current}.html']

    def get_form_initial(self, step):
        initial = super().get_form_initial(step)
        if step == '0':
            initial['division'] = self.division_id
        return initial
    
    # セッションに保存されたデータをhtmlで使えるようにする
    def get_context_data(self, form, **kwargs):
        # コンテキストデータを取得
        context = super().get_context_data(form=form, **kwargs)
        context['division_id'] = self.kwargs.get('division_id')
        step_data = self.request.session.get('step_data_0', {})  # 1ページ目のデータを取得
        print("Step 0 Data:", step_data)  # コンソールに出力
                
        context.update({
            'crime_name': step_data.get('crime_name', ''),
            'crime_name_second': step_data.get('crime_name_second', ''),
            'crime_start_date': step_data.get('crime_start_date', ''),
            'crime_start_time': step_data.get('crime_start_time', ''),
            'crime_end_date': step_data.get('crime_end_date', ''),
            'crime_end_time': step_data.get('crime_end_time', ''),
            'crime_place': step_data.get('crime_place', ''),
            'google_maps_api_key': settings.GOOGLE_MAPS_API_KEY,
        })  
        return context

    def done(self, form_list, **kwargs):
        crime_id = self.request.session.get('crime_id')
        if crime_id:
            crime = Crime.objects.get(id=crime_id)
        else:
            crime = form_list[0].save(commit=False)
            crime.division_id = self.division_id
            crime.save()
            self.request.session['crime_id'] = crime.id  # セッションにcrime_idを保存

        for form in form_list[1:]:
            form_instance = form.save(commit=False)
            for field, value in form.cleaned_data.items():
                setattr(crime, field, value)
            crime.save()

        self.request.session.pop('crime_id', None)  # セッションからcrime_idを削除
        return redirect(reverse_lazy('crime_list', kwargs={'division_id': self.division_id}))



class CrimeDelete(DeleteView):
    model = Crime
    # 削除後にリダイレクトするURL（例：ホームページやリストビューへ）
    def get_success_url(self):
        # 削除されたCrimeオブジェクトが属していたDivisionのIDを取得
        division_id = self.object.division_id
        # division_idを用いてリダイレクト先のURLを生成
        return reverse_lazy('crime_list', kwargs={'division_id': division_id})


class CrimeUpdate(UpdateView):
    model = Crime
    fields = [
        'crime_name', 
        'crime_name_second', 
        'crime_start_date', 
        'crime_start_time', 
        'crime_end_date', 
        'crime_end_time', 
        'crime_place', 
        'crime_fact',
        'suspect_honseki',
        'suspect_address',
        'suspect_job',
        'suspect_name',
        'suspect_birthday',
    ]
    template_name = 'crime_update.html'

    def get_success_url(self):
        # 更新後にcrime_detailページに戻る
        return reverse_lazy('crime_detail', kwargs={'pk': self.object.pk})
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['crime_id'] = self.get_object().id
        return context



def japanese_era_format(date):
    if date is None:
        return ''  # 日付がNoneの場合は空文字列を返す
    # 和暦表示への変換ロジックをここに実装
    # 仮の実装として、西暦をそのまま文字列にして返します
    if date >= datetime.date(2019, 5, 1):
        era_name = "令和"
        era_year = date.year - 2018
    elif date >= datetime.date(1989, 1, 8):
        era_name = "平成"
        era_year = date.year - 1988
    else:
        era_name = "昭和"  # 仮の処理、他の年号についても同様に追加する
        era_year = date.year - 1925  # 仮の処理、実際の計算は年号によって異なる

    if era_year == 1:
        era_year_str = "元年"
    else:
        era_year_str = f"{era_year}年"

    return f"{era_name}{era_year_str}{date.month}月{date.day}日"

def japanese_time_format(time):
    if time is None:
        return ''  # 日付がNoneの場合は空文字列を返す
    # カスタム時間フォーマットへの変換ロジックをここに実装
    # 仮の実装として、時間をそのまま文字列にして返します
    if time:
        return time.strftime("%H時%M分")
    return ''


def generate_report(request, pk):
    if request.method == 'POST' and request.FILES.get('docxFile'):
        docx_file = request.FILES['docxFile']
        file_path = default_storage.save('docx_templates/' + docx_file.name, docx_file)
        full_file_path = default_storage.path(file_path)

        crime = Crime.objects.get(pk=pk)
        doc = DocxTemplate(full_file_path)
        context = {
        'division': crime.division.name,
        'crime_name': crime.crime_name, 
        'crime_fact': crime.crime_fact, 
        'crime_start_date': japanese_era_format(crime.crime_start_date),
        'crime_start_time': japanese_time_format(crime.crime_start_time),
        'crime_end_date': japanese_era_format(crime.crime_end_date),
        'crime_end_time': japanese_era_format(crime.crime_end_date),
        'crime_place': crime.crime_place,
        'suspect_honseki': crime.suspect_honseki,
        'suspect_address': crime.suspect_address,
        'suspect_job': crime.suspect_job,
        'suspect_name': crime.suspect_name,
        'suspect_birthday': japanese_era_format(crime.suspect_birthday),
        }
        doc.render(context)

        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
        response['Content-Disposition'] = f'attachment; filename="generated_report_{crime.pk}.docx"'
        doc.save(response)

        # 一時ファイルを削除
        default_storage.delete(file_path)

        return response
    else:
        # 適切なエラーメッセージを返す。
        return HttpResponse(status=400, content='Invalid request')


def load_crime_data():
    with open('data/crime_types.json', 'r', encoding='utf-8') as file:
        return json.load(file)

crime_data = load_crime_data()


def suggest_crime_name(request):
    input_text = request.GET.get('q', '')  # URLからクエリパラメータを取得
    suggestions = [crime for crime in crime_data["罪名"] if crime.startswith(input_text)]
    return JsonResponse(suggestions, safe=False)
