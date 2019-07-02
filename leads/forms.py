from django import forms
from leads.models import Lead
from common.models import Comment, Attachments


class LeadForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        apartments = kwargs.pop('apartments', [])
        super(LeadForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs = {"class": "form-control"}
        self.fields['apartments'].queryset = apartments
        self.fields['phone'].required = True
        self.fields['birthday'] = forms.CharField(widget=forms.TextInput(attrs={'autocomplete': 'off'}))
        self.fields['birthday'].required = True
        self.fields['gender'].required = True
        for key, value in self.fields.items():
            if key == 'phone':
                value.widget.attrs['placeholder'] = 'Введите номер телефона'
            else:
                value.widget.attrs['placeholder'] = value.label

        self.fields['phone'].widget.attrs.update({
            'placeholder': '+7 777-777-77-77'})

    class Meta:
        model = Lead
        fields = (
            'name',
            'gender',
            'account_name',
            'phone',
            'email'
            , 'status'
            , 'source',
            'birthday',
            'address',
            'description',
            'debt',
            'status_of_work_with_debt',
            'garbage_payment',
            'passport_date',
            'passport_series',
            'passport_id',
            'issued_by',
            'unit_code',
            'type_of_passport',
            'birthday_reminder',
            'hard_case',
            'loyal',
            'vip',
            'calls',
            'sms',
            'mail',
            'comments',
            'apartments'
        )

    def clean_phone(self):
        client_phone = self.cleaned_data.get('phone', None)
        try:
            if int(client_phone) and not client_phone.isalpha():
                ph_length = str(client_phone)
                if len(ph_length) < 10 or len(ph_length) > 13:
                    raise forms.ValidationError('Phone number must be minimum 10 Digits and maximum of 13 Digits')
        except(ValueError):
            raise forms.ValidationError('Phone Number should contain only Numbers')
        return client_phone


# class PassportForm(forms.ModelForm):
#     class Meta:
#         model = Passport
#         fields = (
#             'date_of_issue',
#         )


class LeadCommentForm(forms.ModelForm):
    comment = forms.CharField(max_length=64, required=True)

    class Meta:
        model = Comment
        fields = ('comment', 'lead', 'commented_by')


class LeadAttachmentForm(forms.ModelForm):
    attachment = forms.FileField(max_length=1001, required=True)

    class Meta:
        model = Attachments
        fields = ('attachment', 'lead')
