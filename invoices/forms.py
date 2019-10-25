from django import forms
from .models import Invoice
from apartments.models import Apartment


class InvoiceModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.__str__() + " (" + str(obj.number_of_business_account) + ")"


class InvoiceForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(InvoiceForm, self).__init__(*args, **kwargs)

        self.fields['apartment'] = InvoiceModelChoiceField(
            widget=forms.widgets.Select(attrs={'class': 'select2'}),
            label="Помещение (№ лиц. счета)", queryset=Apartment.objects.all())

    class Meta:
        model = Invoice
        fields = ('apartment', 'name', 'accrued', 'paid')
