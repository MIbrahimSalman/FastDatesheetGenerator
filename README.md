# FastDatesheetGenerator

## Project Description

FastDatesheetGenerator is a Django-based web application that allows university administrators to upload an Excel file containing a university datesheet. The system extracts course codes from the uploaded file, displays them in a dropdown menu for students to select, shows a filtered table based on the selected courses, and allows users to download the customized datesheet as a PDF. Only the admin can upload new datesheets, and the previous one is automatically replaced.

## Project Structure

- A Django project with one app, `datesheet_app`.
- Uses pandas for reading Excel files.
- Stores the uploaded file in a private directory.
- Uses Django’s forms for uploading files.
- Uses Django templates to display the datesheet.
- Uses reportlab or xhtml2pdf to generate a downloadable PDF.

## Required Features

1. **Upload System**
   - Create a file upload form in Django where only the admin can upload an Excel file.
   - When a new file is uploaded, delete the previous one to replace it.
   - Store the uploaded file in `media/uploads/` (or a private location).

2. **Extracting Course Codes**
   - Read the uploaded Excel file using pandas and extract unique course codes.
   - Store them in a list to populate a dropdown menu.

3. **Filtering the Datesheet**
   - When a student selects courses from the dropdown, display the filtered timetable.
   - Use Django’s `views.py` to process form data and filter results.

4. **Displaying & Downloading**
   - Show the customized datesheet in a clean, formatted table using Django templates.
   - Provide a button to generate and download the filtered datesheet as a PDF.

5. **Security & Access Control**
   - Ensure only the admin can upload new files.
   - Users should only see the processed output and not access the original file.
   - Prevent direct access to uploaded files via URLs.

## Setup Instructions

1. Clone the repository:
   ```bash
   git clone https://github.com/githubnext/FastDatesheetGenerator.git
   cd FastDatesheetGenerator
   ```

2. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Apply migrations:
   ```bash
   python manage.py migrate
   ```

5. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```

6. Run the development server:
   ```bash
   python manage.py runserver
   ```

## Usage Instructions

1. **Admin Uploads Datesheet**
   - Log in to the admin panel.
   - Upload the Excel file containing the datesheet.

2. **Student Selects Courses**
   - Visit the homepage.
   - Select courses from the dropdown menu to filter the datesheet.

3. **Download Customized Datesheet**
   - Click the button to generate and download the filtered datesheet as a PDF.
