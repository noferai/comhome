from django import forms
from requests.models import Request
from common.models import Comment, Attachments


class RequestForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        assigned_users = kwargs.pop('assigned_to', [])
        homeowners = kwargs.pop('homeowners', [])
        super(RequestForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs = {"class": "form-control"}
        self.fields['description'].widget.attrs.update({
            'rows': '6'})
        self.fields['applicant'] = forms.ModelChoiceField(widget=forms.widgets.Select(attrs={'class': 'select2'}),
                                                           queryset=homeowners)
        self.fields['assigned_to'] = forms.ModelMultipleChoiceField(widget=forms.widgets.SelectMultiple(attrs={'class': 'select2'}),
                                                                    queryset=assigned_users, required=False)
        self.fields['closed_on'].required = False

    class Meta:
        model = Request
        fields = ('assigned_to', 'status', 'priority', 'request_type', 'closed_on', 'description', 'applicant')


class RequestCommentForm(forms.ModelForm):
    comment = forms.CharField(max_length=64, required=True)

    class Meta:
        model = Comment
        fields = ('comment', 'request', 'commented_by', )


class RequestAttachmentForm(forms.ModelForm):
    attachment = forms.FileField(max_length=1001, required=True)

    class Meta:
        model = Attachments
        fields = ('attachment', 'request')
