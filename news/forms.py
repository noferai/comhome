from django import forms
from .models import Entry


class EntryForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(EntryForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs = {"class": "form-control"}
        self.fields['title'].widget.attrs.update({'rows': '1'})
        self.fields['text'].widget.attrs.update({'rows': '10'})
        self.fields['author'].required = False

    class Meta:
        model = Entry
        fields = ('title', 'author', 'text')