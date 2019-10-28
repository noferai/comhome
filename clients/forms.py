from django import forms
from .models import Client
from phones.models import PhoneNumber
from documents.models import Document
from phones.forms import PhoneForm
from documents.forms import DocumentForm


class ClientForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ClientForm, self).__init__(*args, **kwargs)
        self.fields['birthday'] = forms.DateField(
            widget=forms.widgets.DateInput(attrs={'class': 'form-control date'}), label="Дата рождения")
        self.fields['email'] = forms.EmailField(widget=forms.widgets.EmailInput)
        self.fields['password'] = forms.CharField(widget=forms.PasswordInput, label="Пароль")
        for field_name in ['type', 'apartments', 'gender']:
            self.fields[field_name].widget.attrs.update({'class': 'form-control select2'})
        for field_name in ['calls', 'sms', 'mail']:
            self.fields[field_name] = forms.BooleanField(widget=forms.widgets.CheckboxInput,
                                                         label=self.fields[field_name].label, initial=False,
                                                         required=False)

    def save(self, commit=True):
        client = super().save(commit=False)
        client.set_password(self.cleaned_data["password"])
        if commit:
            client.save()
        return client

    class Meta:
        model = Client
        fields = ('type', 'name', 'gender', 'email', 'birthday', 'car_numbers', 'registration', 'calls', 'sms', 'mail',
                  'apartments', 'passport', 'password')


PhoneFormSet = forms.inlineformset_factory(Client, PhoneNumber, form=PhoneForm, extra=1)
DocumentFormSet = forms.inlineformset_factory(Client, Document, form=DocumentForm, extra=1)
