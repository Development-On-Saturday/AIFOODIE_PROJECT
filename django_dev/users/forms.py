from django import forms
from . import models


class RegisterForm(forms.ModelForm):

    password = forms.CharField(label='password', widget=forms.PasswordInput)
    confirm_password = forms.CharField(label='confirm_password', widget=forms.PasswordInput)

    class Meta:
        model = models.User
        fields = ['username', 'first_name', 'last_name', 'email']

    def clean_confirm_password(self):
        cleaned_data = self.cleaned_data
        if cleaned_data['password'] != cleaned_data['confirm_password']:
            raise forms.ValidationError("Password does not match")

        return cleaned_data['confirm_password']


class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder" : "Email Address"}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Password"})
    )

    def clean(self):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        try:
            user = models.User.objects.get(email=email)
            if user.check_password(password):
                return self.cleaned_data
            else:
                self.add_error("password", forms.ValidationError("Password is wrong"))
        except models.User.DoesNotExist:
            self.add_error("email", forms.ValidationError("User does not exist"))
