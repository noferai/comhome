from django import forms
from requests.models import Request


class RequestForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        assigned_users = kwargs.pop('assigned_to', [])
        homeowners = kwargs.pop('homeowners', [])
        apartments = kwargs.pop('apartments', [])
        super(RequestForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs = {"class": "form-control"}
        self.fields['description'].widget.attrs.update({
            'rows': '4'})
        self.fields['applicant'] = forms.ModelChoiceField(widget=forms.widgets.Select(attrs={'class': 'select2'}),
                                                          queryset=homeowners, label='Заявитель')
        self.fields['assigned_to'] = forms.ModelMultipleChoiceField(
            widget=forms.widgets.SelectMultiple(attrs={'class': 'select2'}),
            queryset=assigned_users, required=False, label='Исполнители')
        self.fields['apartment'] = forms.ModelChoiceField(widget=forms.widgets.Select(attrs={'class': 'select2'}),
                                                          queryset=apartments, label='Квартира')

    class Meta:
        model = Request
        fields = (
            'assigned_to', 'status', 'priority', 'request_type', 'applicant', 'apartment', 'closed_on', 'description')
