from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from .forms import DatesheetUploadForm
from .models import Datesheet
import pandas as pd
from reportlab.pdfgen import canvas
from io import BytesIO
from django.views.decorators.http import require_POST
from django.template.loader import get_template
from xhtml2pdf import pisa

def clean_datesheet(file_path):
    """
    Reads the Excel file and extracts exam details including day, date, time, course code, and course name.
    Assumes the following structure:
      - Row 0: Metadata (e.g. "Spring 2025 Semester")
      - Row 1: Column headers (e.g. "Day", "Date", "Course Code 1", "Course Name 1", ...)
      - Row 2: Time row; each course column pair (code, name) shares the same time from this row.
      - Row 3+: Data rows.
    The date is converted to a string (YYYY-MM-DD) and missing values are replaced with empty strings.
    """
    df = pd.read_excel(file_path, header=None, sheet_name="Complete")
    # Use the third row (index 2) for time values
    time_row = df.iloc[2]
    data = df.iloc[3:].reset_index(drop=True)
    courses = []
    ncols = data.shape[1]
    for _, row in data.iterrows():
        day = row[0] if pd.notna(row[0]) else ""
        try:
            date_dt = pd.to_datetime(row[1], errors="coerce")
            if pd.isna(date_dt):
                continue
            date_str = date_dt.strftime("%Y-%m-%d")
        except Exception:
            continue
        # Iterate over course columns in pairs (course code, course name)
        for j in range(2, ncols, 2):
            course_code = row[j] if pd.notna(row[j]) else ""
            if course_code != "":
                course_name = row[j+1] if j+1 < ncols and pd.notna(row[j+1]) else ""
                time_slot = ""
                # For each pair, the time is taken from the time_row (using the same column index as the course name)
                if j+1 < ncols and pd.notna(time_row[j+1]):
                    time_slot = str(time_row[j+1]).strip()
                courses.append({
                    "day": str(day).strip(),
                    "date": date_str,
                    "time": time_slot,
                    "course_code": str(course_code).strip(),
                    "course_name": str(course_name).strip()
                })
    return courses

# @login_required
def upload_datesheet(request):
    if request.method == 'POST':
        form = DatesheetUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # Clear previous datesheet and selected exams
            Datesheet.objects.all().delete()
            form.save()
            request.session['selected_courses'] = []
            return redirect('display_datesheet')
    else:
        form = DatesheetUploadForm()
    return render(request, 'upload.html', {'form': form})

# @login_required
def display_datesheet(request):
    """
    Renders the main page with a search bar for exams and shows the selected exams.
    """
    selected_exams = request.session.get('selected_courses', [])
    context = {
        'selected_exams': selected_exams,
    }
    return render(request, 'datesheet.html', context)

# @login_required
def search_courses(request):
    """
    AJAX endpoint to search courses based on the query (searches both course code and course name).
    """
    datesheet = Datesheet.objects.first()
    if not datesheet:
        return JsonResponse({"courses": []})
    all_courses = clean_datesheet(datesheet.file.path)
    query = request.GET.get("query", "").lower()
    filtered = [
        course for course in all_courses
        if query in course["course_code"].lower() or query in course["course_name"].lower()
    ]
    filtered = sorted(filtered, key=lambda x: (x["date"], x["time"]))
    return JsonResponse({"courses": filtered})

@require_POST
# @login_required
def add_exam(request):
    """
    Adds an exam to the selected courses in session.
    """
    exam = {
        'day': request.POST.get('day'),
        'date': request.POST.get('date'),  # Expected format "YYYY-MM-DD"
        'time': request.POST.get('time'),
        'course_code': request.POST.get('course_code'),
        'course_name': request.POST.get('course_name'),
    }
    selected = request.session.get('selected_courses', [])
    if exam not in selected:
        selected.append(exam)
        selected = sorted(selected, key=lambda x: (x["date"], x["time"]))
        request.session['selected_courses'] = selected
    return redirect('display_datesheet')

@require_POST
# @login_required
def delete_exam(request):
    """
    Removes an exam from the selected courses in session.
    """
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
    return redirect('display_datesheet')

# @login_required
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
