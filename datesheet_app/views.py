from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
import pandas as pd
from reportlab.pdfgen import canvas
from io import BytesIO
from django.views.decorators.http import require_POST
from django.template.loader import get_template
from xhtml2pdf import pisa

# Import the static datesheet data
from datesheet_data import DATESHEET

def datesheet_view(request):
    return render(request, "datesheet.html")  # Home/landing page

def display_datesheet(request):
    # Use session's selected courses (initially empty)
    selected_exams = request.session.get('selected_courses', [])
    context = {'selected_exams': selected_exams}
    return render(request, 'datesheet.html', context)


def search_courses(request):
    all_courses = DATESHEET  # static data for searching
    query = request.GET.get("query", "").lower()
    filtered = [
        course for course in all_courses
        if query in course["course_code"].lower() or query in course["course_name"].lower()
    ]
    filtered = sorted(filtered, key=lambda x: (x["date"], x["time"]))
    return JsonResponse({"courses": filtered})


@require_POST
def add_exam(request):
    exam = {
        'day': request.POST.get('day'),
        'date': request.POST.get('date'),
        'time': request.POST.get('time'),
        'course_code': request.POST.get('course_code'),
        'course_name': request.POST.get('course_name'),
    }
    selected = request.session.get('selected_courses', [])
    if exam not in selected:
        selected.append(exam)
        selected = sorted(selected, key=lambda x: (x["date"], x["time"]))
        request.session['selected_courses'] = selected
    # Change redirect to use a URL name that exists, e.g., 'home'
    return redirect('home')

@require_POST
def delete_exam(request):
    course_code = request.POST.get('course_code')
    date = request.POST.get('date')
    time = request.POST.get('time')
    selected = request.session.get('selected_courses', [])
    new_selected = [
        exam for exam in selected
        if not (exam['course_code'] == course_code and exam['date'] == date and exam['time'] == time)
    ]
    new_selected = sorted(new_selected, key=lambda x: (x["date"], x["time"]))
    request.session['selected_courses'] = new_selected
    return redirect('home')

def download_datesheet(request):
    """
    Generates a PDF datesheet using the selected exams.
    The PDF mirrors the web page layout (except for the Action column).
    """
    selected = request.session.get('selected_courses', [])
    if selected:
        sorted_exams = sorted(selected, key=lambda x: (x["date"], x["time"]))
        template = get_template('pdf_datesheet.html')
        html = template.render({'selected_exams': sorted_exams})
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="datesheet.pdf"'
        pisa_status = pisa.CreatePDF(html, dest=response)
        if pisa_status.err:
            return HttpResponse("Error generating PDF", status=500)
        return response
    return HttpResponse("No exams selected.")
