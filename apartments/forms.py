from django import forms
from .models import Apartment
from documents.models import Document
from documents.forms import DocumentForm


class ApartmentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        addresses = kwargs.pop('addresses', [])
        super(ApartmentForm, self).__init__(*args, **kwargs)

        self.fields['address'] = forms.ModelChoiceField(
            widget=forms.widgets.Select(attrs={'class': 'select2'}),
            queryset=addresses, label="Адрес")

    class Meta:
        model = Apartment
        fields = ['number_of_business_account', 'address', 'apartment_number', 'entrance', 'floor', 'number_of_rooms', 'area',
                  'part_of_area', 'status']


DocumentFormSet = forms.inlineformset_factory(Apartment, Document, form=DocumentForm, extra=1, can_delete=True)
