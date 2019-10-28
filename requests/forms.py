from django import forms
from requests.models import Request


class RequestForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(RequestForm, self).__init__(*args, **kwargs)
        self.fields['description'].widget.attrs.update({'rows': '4'})
        for field_name in ['applicant', 'assigned_to', 'apartment', 'status', 'priority', 'request_type']:
            self.fields[field_name].widget.attrs.update({'class': 'form-control select2'})

    class Meta:
        model = Request
        fields = (
            'assigned_to', 'status', 'priority', 'request_type', 'applicant', 'apartment', 'closed_on', 'description')
