from django import forms
from .models import Entry


class EntryForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(EntryForm, self).__init__(*args, **kwargs)
        self.fields['text'].widget.attrs.update({'rows': '10'})
        self.fields['status'].widget.attrs.update({'class': 'form-control select2'})

    class Meta:
        model = Entry
        fields = ['title', 'text', 'status']
