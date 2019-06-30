from django import forms
from .models import Account
from common.models import Comment, Attachments


class AccountForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(AccountForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs = {"class": "form-control"}
        self.fields['description'].widget.attrs.update({'rows': '8'})
        self.fields['email'].required = False
        for key, value in self.fields.items():
            if key == 'phone':
                value.widget.attrs['placeholder'] = "+7 777-777-77-77"
            else:
                value.widget.attrs['placeholder'] = value.label

    class Meta:
        model = Account
        fields = ('name', 'phone', 'email', 'industry', 'description')


class AccountCommentForm(forms.ModelForm):
    comment = forms.CharField(max_length=64, required=True)

    class Meta:
        model = Comment
        fields = ('comment', 'account', 'commented_by')


class AccountAttachmentForm(forms.ModelForm):
    attachment = forms.FileField(max_length=1001, required=True)

    class Meta:
        model = Attachments
        fields = ('attachment', 'account')
