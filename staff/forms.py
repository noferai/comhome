from django import forms
from phonenumber_field.widgets import PhoneNumberInternationalFallbackWidget
from phonenumber_field.formfields import PhoneNumberField
from .models import Staff


class StaffForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(StaffForm, self).__init__(*args, **kwargs)

        self.fields['phone'] = PhoneNumberField(
            widget=PhoneNumberInternationalFallbackWidget(attrs={'class': 'form-control international-inputmask'}),
            label="Телефон")
        self.fields['occupation'].widget.attrs.update({'class': 'form-control select2'})

    class Meta:
        model = Staff
        fields = ('name', 'phone', 'email', 'occupation')
