from django import forms
from .models import Staff
from common.models import Comment, Attachments


class StaffForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(StaffForm, self).__init__(*args, **kwargs)
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
        model = Staff
        fields = ('name', 'phone', 'email', 'industry', 'description')


class StaffCommentForm(forms.ModelForm):
    comment = forms.CharField(max_length=64, required=True)

    class Meta:
        model = Comment
        fields = ('comment', 'staff', 'commented_by')


class StaffAttachmentForm(forms.ModelForm):
    attachment = forms.FileField(max_length=1001, required=True)

    class Meta:
        model = Attachments
        fields = ('attachment', 'staff')
