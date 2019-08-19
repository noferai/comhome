from django import forms
from .models import Address


class AddressForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AddressForm, self).__init__(*args, **kwargs)

        self.fields['city'] = forms.ChoiceField(
            widget=forms.widgets.Select(attrs={'class': 'select2'}),
            label="Город", choices=self.fields['city'].choices, initial=self.fields['city'].choices[1])

    class Meta:
        model = Address
        fields = ['city', 'street', 'building']
