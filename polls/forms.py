from django import forms
from .models import Poll, Choice


class PollForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(PollForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Poll
        fields = ['question', 'status']


class ChoiceForm(forms.ModelForm):
    class Meta:
        model = Choice
        exclude = ('votes',)


ChoiceFormSet = forms.inlineformset_factory(Poll, Choice, form=ChoiceForm, extra=1, can_delete=False)
