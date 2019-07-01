from django import forms
from cases.models import Case
from common.models import Comment, Attachments


class CaseForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        assigned_users = kwargs.pop('assigned_to', [])
        super(CaseForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs = {"class": "form-control"}
        self.fields['description'].widget.attrs.update({
            'rows': '6'})
        self.fields['assigned_to'].queryset = assigned_users
        self.fields['assigned_to'].required = False
        self.fields['closed_on'].required = False
        for key, value in self.fields.items():
            value.widget.attrs['placeholder'] = value.label

    class Meta:
        model = Case
        fields = ('assigned_to', 'status', 'priority', 'request_type', 'closed_on', 'description')

    def clean_name(self):
        name = self.cleaned_data['name']
        case = Case.objects.filter(name__iexact=name).exclude(id=self.instance.id)
        if case:
            raise forms.ValidationError("Такая заявка уже есть")
        return name


class CaseCommentForm(forms.ModelForm):
    comment = forms.CharField(max_length=64, required=True)

    class Meta:
        model = Comment

        fields = ('comment', 'case', 'commented_by', )


class CaseAttachmentForm(forms.ModelForm):
    attachment = forms.FileField(max_length=1001, required=True)

    class Meta:
        model = Attachments
        fields = ('attachment', 'case')
