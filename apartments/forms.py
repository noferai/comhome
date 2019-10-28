from django import forms
from .models import Apartment
from documents.models import Document
from documents.forms import DocumentForm


class ApartmentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ApartmentForm, self).__init__(*args, **kwargs)
        for field_name in ['type', 'address']:
            self.fields[field_name].widget.attrs.update({'class': 'form-control select2'})

    class Meta:
        model = Apartment
        fields = ['number_of_business_account', 'address', 'apartment_number', 'entrance', 'floor', 'number_of_rooms',
                  'area', 'type']


DocumentFormSet = forms.inlineformset_factory(Apartment, Document, form=DocumentForm, extra=1, can_delete=True)
