from django import forms
from .models import Datesheet

class DatesheetUploadForm(forms.ModelForm):
    class Meta:
        model = Datesheet
        fields = ['file']
