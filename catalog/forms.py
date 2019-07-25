from django import forms
from .models import Address


class AddressForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(AddressForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs = {"class": "form-control"}

    class Meta:
        model = Address
        fields = ('address_str',)
