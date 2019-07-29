from django import forms
from requests.models import Request
from common.models import Comment, Attachments


class RequestForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        assigned_users = kwargs.pop('assigned_to', [])
        homeowners = kwargs.pop('homeowner', [])
        super(RequestForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs = {"class": "form-control"}
        self.fields['description'].widget.attrs.update({
            'rows': '6'})
        self.fields['assigned_to'].queryset = assigned_users
        self.fields['assigned_to'].required = False
        self.fields['closed_on'].required = False
        for key, value in self.fields.items():
            value.widget.attrs['placeholder'] = value.label

    class Meta:
        model = Request
        fields = ('assigned_to', 'status', 'priority', 'request_type', 'closed_on', 'description', 'homeowner')


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
