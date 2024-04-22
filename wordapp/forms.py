from django import forms
from django.forms import ModelForm
from .models import Crime

class CrimeInfoForm(ModelForm):
    class Meta:
        model = Crime
        fields = ['crime_name', 'crime_name_second', 'crime_start_date', 'crime_start_time', 'crime_end_date', 'crime_end_time', 'crime_place']
        labels = {
            'crime_name': '罪名',
            'crime_name_second': '中種別',
            'crime_start_date': '発生日',
            'crime_start_time': '発生時刻',
            'crime_end_date': '終了日',
            'crime_end_time': '終了時刻',
            'crime_place': '発生場所',
        }
        widgets = {
            'crime_start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'crime_start_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'crime_end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'crime_end_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'crime_place': forms.TextInput(attrs={'class': 'form-control'}),
            'crime_name': forms.TextInput(attrs={'class': 'form-control'}),
            'crime_name_second': forms.TextInput(attrs={'class': 'form-control'}),
        }
    # def __init__(self, *args, **kwargs):
    #     super(CrimeInfoForm, self).__init__(*args, **kwargs)
    #     self.fields['crime_name'].choices = [('assault', '暴行'), ('injury', '傷害')]
    #     self.fields['crime_name_second'].choices = []
    #     self.fields['crime_name'].widget.attrs.update({'onchange': 'updateSecondCategory();'})


class CrimeDetailForm(ModelForm):
    class Meta:
        model = Crime
        fields = ['crime_fact']
        labels = {
            'crime_fact': '犯罪事実',
        }
        widgets = {
            'crime_fact': forms.Textarea(attrs={'cols': 40, 'rows': 5, 'class': 'form-control'}),
        }

class SuspectInfoForm(ModelForm):
    class Meta:
        model = Crime
        fields = ['suspect_honseki', 'suspect_address', 'suspect_job', 'suspect_name', 'suspect_birthday']
        labels = {
            'suspect_honseki': '本籍地',
            'suspect_address': '住所',
            'suspect_job': '職業',
            'suspect_name': '名前',
            'suspect_birthday': '生年月日',
        }
        widgets = {
            'suspect_honseki': forms.TextInput(attrs={'class': 'form-control'}),
            'suspect_address': forms.TextInput(attrs={'class': 'form-control'}),
            'suspect_job': forms.TextInput(attrs={'class': 'form-control'}),
            'suspect_name': forms.TextInput(attrs={'class': 'form-control'}),
            'suspect_birthday': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }