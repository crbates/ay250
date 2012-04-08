#Simple form for storing the file field
from django import forms

class DocumentForm(forms.Form):
    docfile = forms.FileField(label='Select a file' )
