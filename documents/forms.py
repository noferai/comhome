from django import forms
from .models import Document


class DocumentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(DocumentForm, self).__init__(*args, **kwargs)
        self.fields['date'].widget.attrs.update({'class': 'form-control date'})
        self.fields['type'].widget.attrs.update({'class': 'form-control select2'})
        self.fields['note'].widget.attrs.update({'rows': '3'})

    class Meta:
        model = Document
        fields = ['date', 'type', 'note', 'attachment']
