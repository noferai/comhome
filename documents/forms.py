from django import forms
from .models import Document


class DocumentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(DocumentForm, self).__init__(*args, **kwargs)
        self.fields['date'] = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}), label="Дата")
        self.fields['note'].widget.attrs.update({'rows': '3'})

    class Meta:
        model = Document
        fields = ['date', 'type', 'note', 'attachment']


