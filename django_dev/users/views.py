from django.shortcuts import reverse, redirect
from django.views.generic import FormView
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse_lazy
from django.contrib import messages
from . import forms


class LoginView(FormView):

    template_name = "users/login.html"
    form_class = forms.LoginForm

    def form_valid(self, form):
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, email=email, password=password)
        if user is not None:
            login(self.request, user)
        return super().form_valid(form)

    def get_success_url(self):
        next_arg = self.request.GET.get("next")
        print(next_arg)
        if next_arg is not None:
            return next_arg
        else:
            return reverse("core:index")


class RegisterView(FormView):

    template_name = "users/register.html"
    form_class = forms.RegisterForm
    success_url = reverse_lazy("core:index")

    def form_valid(self, form):
        form.save()
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        print(self.request)
        user = authenticate(self.request, email=email, password=password)
        print(user)
        return super().form_valid(form)

def log_out(request):
    messages.info(request, "See you later")
    logout(request)
    return redirect(reverse("core:index"))