from django.views.generic import View
from django.shortcuts import render, redirect
from .models import Event
from docxtpl import DocxTemplate
from django.http import HttpResponse
import io

class ReportCreateView(View):
    def get(self, request, *args, **kwargs):
        events = Event.objects.all()
        return render(request, 'report_create.html', {'events': events})

    def post(self, request, *args, **kwargs):
        template_name = request.POST.get('template')
        event_id = request.POST.get('event')
        event = Event.objects.get(id=event_id)

        doc = DocxTemplate(f"templates/{template_name}.docx")
        context = {
            '発生日': event.発生日,
            '事件名': event.事件名,
            # その他のフィールドをコンテキストに追加
        }
        doc.render(context)

        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
        response['Content-Disposition'] = 'attachment; filename="report.docx"'

        with io.BytesIO() as doc_io:
            doc.save(doc_io)
            doc_io.seek(0)
            response.write(doc_io.read())

        return response