from django import forms
from .models import Homeowner
from phones.models import PhoneNumber
from phones.forms import PhoneForm


class HomeownerForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        apartments = kwargs.pop('apartments', [])
        super(HomeownerForm, self).__init__(*args, **kwargs)
        self.fields['birthday'] = forms.DateField(
            widget=forms.widgets.DateInput(attrs={'type': 'date'}), label="День рождения")
        self.fields['passport_date'] = forms.DateField(
            widget=forms.widgets.DateInput(attrs={'type': 'date'}), label="Дата выдачи")
        self.fields['apartments'] = forms.ModelMultipleChoiceField(
            widget=forms.widgets.SelectMultiple(attrs={'class': 'select2'}),
            queryset=apartments, label="Квартиры")
        for name in ['birthday_reminder', 'hard_case', 'loyal', 'vip', 'calls', 'sms', 'mail']:
            self.fields[name] = forms.BooleanField(widget=forms.widgets.CheckboxInput,
                                                   label=self.fields[name].label, initial=False, required=False)

    def save(self, commit=True):
        homeowner = super().save(commit=False)
        homeowner.set_password(self.cleaned_data["password"])
        if commit:
            homeowner.save()
        return homeowner

    class Meta:
        model = Homeowner
        fields = ('name', 'gender', 'email', 'birthday', 'debt', 'status_of_work_with_debt',
                  'garbage_payment', 'passport_date', 'passport_series', 'passport_id', 'issued_by', 'unit_code',
                  'type_of_passport', 'birthday_reminder', 'hard_case', 'loyal', 'vip', 'calls', 'sms', 'mail',
                  'apartments', 'password')


PhoneFormSet = forms.inlineformset_factory(Homeowner, PhoneNumber, form=PhoneForm, extra=1, can_delete=False)
