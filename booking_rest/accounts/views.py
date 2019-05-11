from django.views import View
from django.views.generic import FormView
from django.views.generic import CreateView
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.urls import reverse_lazy

from accounts.forms import *


class RegistrationFormView(CreateView):
    form_class = RegistrationForm
    template_name = 'accounts/registration.html'
    success_url = reverse_lazy('login_url')

    def form_valid(self, form):
        account = form.instance
        account.set_password(form.cleaned_data['password'])

        return super().form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('control_panel_url')
        return super().dispatch(request, *args, **kwargs)


class LoginFormView(FormView):
    form_class = LoginForm
    template_name = 'accounts/login.html'
    success_url = reverse_lazy('control_panel_url')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('control_panel_url')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']

        account = authenticate(self.request, username=username, password=password)

        if account:
            login(self.request, account)
            return super().form_valid(form)
        else:
            return redirect(reverse_lazy('login_url'))


class AccountLogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)

        return redirect(reverse_lazy('login_url'))
