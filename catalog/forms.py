from django import forms
from .models import Address, Services


class AddressForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(AddressForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs = {"class": "form-control"}

    class Meta:
        model = Address
        fields = ('address',)


class ServicesForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ServicesForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs = {"class": "form-control"}

    class Meta:
        model = Services
        fields = ('name_of_service', 'debt_at_beg_of_period', 'accrued',
                  'recalculations', 'paid', 'debt_at_end_of_period',)
