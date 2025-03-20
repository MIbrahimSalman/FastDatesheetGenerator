from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from .forms import DatesheetUploadForm
from .models import Datesheet
import pandas as pd
from reportlab.pdfgen import canvas
from io import BytesIO

@login_required
def upload_datesheet(request):
    if request.method == 'POST':
        form = DatesheetUploadForm(request.POST, request.FILES)
        if form.is_valid():
            Datesheet.objects.all().delete()  # Delete previous datesheet
            form.save()
            return redirect('datesheet')
    else:
        form = DatesheetUploadForm()
    return render(request, 'upload.html', {'form': form})

def display_datesheet(request):
    datesheet = Datesheet.objects.first()
    if datesheet:
        df = pd.read_excel(datesheet.file.path)
        courses = df['Course Code'].unique()
        selected_courses = request.GET.getlist('courses')
        if selected_courses:
            df = df[df['Course Code'].isin(selected_courses)]
        return render(request, 'datesheet.html', {'datesheet': df.to_html(), 'courses': courses})
    return HttpResponse("No datesheet uploaded.")

def download_datesheet(request):
    datesheet = Datesheet.objects.first()
    if datesheet:
        df = pd.read_excel(datesheet.file.path)
        selected_courses = request.GET.getlist('courses')
        if selected_courses:
            df = df[df['Course Code'].isin(selected_courses)]
        buffer = BytesIO()
        p = canvas.Canvas(buffer)
        p.drawString(100, 100, df.to_string())
        p.showPage()
        p.save()
        buffer.seek(0)
        return HttpResponse(buffer, content_type='application/pdf')
    return HttpResponse("No datesheet uploaded.")
