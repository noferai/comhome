from django import forms
from homeowners.models import Homeowner
from common.models import Comment, Attachments


class HomeownerForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        apartments = kwargs.pop('apartments', [])
        super(HomeownerForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs = {"class": "form-control"}
        self.fields['apartments'] = forms.ModelMultipleChoiceField(widget=forms.widgets.SelectMultiple(attrs={'class': 'select2'}),
                                                                   queryset=apartments)
        self.fields['birthday'] = forms.CharField(widget=forms.TextInput(attrs={'autocomplete': 'off'}))

        self.fields['phone'].widget.attrs.update({
            'placeholder': '+7 777-777-77-77'})

    class Meta:
        model = Homeowner
        fields = ('name', 'gender', 'phone', 'email', 'birthday', 'debt', 'status_of_work_with_debt',
                  'garbage_payment', 'passport_date', 'passport_series', 'passport_id', 'issued_by', 'unit_code',
                  'type_of_passport', 'birthday_reminder', 'hard_case', 'loyal', 'vip', 'calls', 'sms', 'mail',
                  'comments', 'apartments')


class HomeownerCommentForm(forms.ModelForm):
    comment = forms.CharField(max_length=64, required=True)

    class Meta:
        model = Comment
        fields = ('comment', 'homeowner', 'commented_by')


class HomeownerAttachmentForm(forms.ModelForm):
    attachment = forms.FileField(max_length=1001, required=True)

    class Meta:
        model = Attachments
        fields = ('attachment', 'homeowner')
