from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import PasswordResetForm
from users.models import User, Admin


class AdminForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Пароль")

    class Meta:
        model = Admin
        fields = ['name', 'email', 'password', 'profile_pic']

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if password:
            if len(password) < 4:
                raise forms.ValidationError(
                    'Слишком короткий пароль')
        return password

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if self.instance.id:
            if self.instance.email != email:
                if not Admin.objects.filter(email=self.cleaned_data.get("email")).exists():
                    return self.cleaned_data.get("email")
                else:
                    raise forms.ValidationError('Этот email уже используется')
            else:
                return self.cleaned_data.get("email")
        else:
            if not Admin.objects.filter(email=self.cleaned_data.get("email")).exists():
                    return self.cleaned_data.get("email")
            else:
                raise forms.ValidationError('Этот email уже используется')


class LoginForm(forms.ModelForm):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['email', 'password']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        super(LoginForm, self).__init__(*args, **kwargs)

    def clean(self):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")

        if email and password:
            self.user = authenticate(email=email, password=password)
            if self.user:
                if not self.user.is_active:
                    raise forms.ValidationError("Аккаунт не активирован")
            else:
                raise forms.ValidationError("Неправильный email или пароль")
        return self.cleaned_data


class ChangePasswordForm(forms.Form):
    CurrentPassword = forms.CharField(max_length=100)
    Newpassword = forms.CharField(max_length=100)
    confirm = forms.CharField(max_length=100)

    def __init__(self, *args, **kwargs):
        super(ChangePasswordForm, self).__init__(*args, **kwargs)

    def clean_confirm(self):
        if len(self.data.get('confirm')) < 4:
            raise forms.ValidationError(
                'Password must be at least 4 characters long!')
        if self.data.get('confirm') != self.cleaned_data.get('Newpassword'):
            raise forms.ValidationError(
                'Confirm password do not match with new password')
        return self.data.get('confirm')


class PasswordResetEmailForm(PasswordResetForm):
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not User.objects.filter(email__iexact=email, is_active=True).exists():
            raise forms.ValidationError("User doesn't exist with this Email")
        return email
