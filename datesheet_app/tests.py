from django.test import TestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import Datesheet
import pandas as pd

class DatesheetUploadTest(TestCase):
    def test_upload_datesheet(self):
        with open('test_datesheet.xlsx', 'rb') as f:
            response = self.client.post(reverse('upload_datesheet'), {'file': f})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Datesheet.objects.count(), 1)

class DatesheetFilterTest(TestCase):
    def setUp(self):
        self.datesheet = Datesheet.objects.create(file=SimpleUploadedFile('test_datesheet.xlsx', b''))
        df = pd.DataFrame({'Course Code': ['CS101', 'CS102', 'CS103']})
        df.to_excel(self.datesheet.file.path, index=False)

    def test_filter_datesheet(self):
        response = self.client.get(reverse('datesheet'), {'courses': ['CS101', 'CS102']})
        self.assertEqual(response.status_code, 200)
        self.assertIn('CS101', response.content.decode())
        self.assertIn('CS102', response.content.decode())
        self.assertNotIn('CS103', response.content.decode())

class DatesheetDownloadTest(TestCase):
    def setUp(self):
        self.datesheet = Datesheet.objects.create(file=SimpleUploadedFile('test_datesheet.xlsx', b''))
        df = pd.DataFrame({'Course Code': ['CS101', 'CS102', 'CS103']})
        df.to_excel(self.datesheet.file.path, index=False)

    def test_download_datesheet(self):
        response = self.client.get(reverse('download_datesheet'), {'courses': ['CS101', 'CS102']})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/pdf')
