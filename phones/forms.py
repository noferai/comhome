from django import forms
from phonenumber_field.widgets import PhoneNumberInternationalFallbackWidget
from phonenumber_field.formfields import PhoneNumberField
from .models import PhoneNumber


class PhoneForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(PhoneForm, self).__init__(*args, **kwargs)
        self.fields['number'] = PhoneNumberField(
            widget=PhoneNumberInternationalFallbackWidget(attrs={'class': 'form-control international-inputmask'}),
            required=True,
            label="Телефон")

    class Meta:
        model = PhoneNumber
        fields = ['number', 'note']
        exclude = ()
