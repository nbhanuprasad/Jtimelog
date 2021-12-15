from django import forms








class formupload(forms.Form):
    f=forms.FileField(label='select a file')
