from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.hashers import check_password
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from ComfortableHome.mixins import AdminRequiredMixin
from django.contrib.auth.views import PasswordResetView
from users.forms import LoginForm, ChangePasswordForm, PasswordResetEmailForm
from django.views.generic import TemplateView, View


class CRMHomeView(AdminRequiredMixin, TemplateView):
    template_name = "crm/index.html"


class LoginView(TemplateView):
    template_name = "crm/login.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_admin:
                return HttpResponseRedirect('/')
            else:
                return HttpResponseRedirect('/client')
        return super(LoginView, self).dispatch(request, *args, **kwargs)

    @staticmethod
    def post(request):
        form = LoginForm(request.POST, request=request)
        if form.is_valid():
            user = authenticate(username=request.POST.get('email'), password=request.POST.get('password'))
            if user is not None:
                if not user.is_active:
                    return render(request, "crm/login.html", {
                        "error": True,
                        "message": "Аккаунт деактивирован"
                    })
                else:
                    login(request, user)
                    if user.is_admin:
                        return HttpResponseRedirect('/')
                    else:
                        return HttpResponseRedirect('/client')
            else:
                return render(request, "crm/login.html", {
                    "error": True,
                    "message": "Аккаунт не найден"
                })
        else:
            return render(request, "crm/login.html", {
                "error": True,
                "message": "Неправильный email или пароль"
            })

#
# class ForgotPasswordView(TemplateView):
#     template_name = "forgot_password.html"


class LogoutView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        logout(request)
        request.session.flush()
        return redirect("users:login")


class ChangePasswordView(LoginRequiredMixin, TemplateView):
    template_name = "change_password.html"

    def post(self, request, *args, **kwargs):
        error, errors = "", ""
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            user = request.user
            if not check_password(request.POST.get('CurrentPassword'), user.password):
                error = "Invalid old password"
            else:
                user.set_password(request.POST.get('Newpassword'))
                user.is_active = True
                user.save()
                return HttpResponseRedirect('/')
        else:
            errors = form.errors
        return render(request, "change_password.html", {'error': error, 'errors': errors})


# class PasswordResetView(PasswordResetView):
#     template_name = 'registration/password_reset_form.html'
#     form_class = PasswordResetEmailForm
#     email_template_name = 'registration/password_reset_email.html'


def handler404(request, exception):
    return render(request, '404.html', status=404)


def handler500(request):
    return render(request, '500.html', status=500)