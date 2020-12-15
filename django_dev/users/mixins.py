from django.contrib import messages
from django.urls import reverse_lazy
from django.shortcuts import redirect, reverse
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin

class LoggedInOnlyView(LoginRequiredMixin):
    login_url= reverse_lazy("users:login")