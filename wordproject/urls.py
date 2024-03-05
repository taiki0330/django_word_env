from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('report/create/', ReportCreateView.as_view(), name='report-create'),
]
