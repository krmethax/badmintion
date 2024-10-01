from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate
from .models import UserBadminton, Court
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm

class RegisterForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = UserBadminton
        fields = ['username', 'first_name', 'last_name', 'role']  # Include 'role'

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        # Filter role choices to exclude 'admin'
        self.fields['role'].choices = [
            ('student', 'นักเรียน'),
            ('teacher', 'ครู'),
        ]

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])  # Hash the password
        if commit:
            user.save()
        return user

class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Username")
    password = forms.CharField(label="Password", widget=forms.PasswordInput)

    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise forms.ValidationError("This account is inactive.", code='inactive')

class CourtForm(forms.ModelForm):
    class Meta:
        model = Court
        fields = ['court_name', 'status']  # Include the fields you want in the form

class ResetPasswordForm(forms.Form):
    username = forms.CharField(label='Username', max_length=150)
    new_password1 = forms.CharField(label='New password', widget=forms.PasswordInput)
    new_password2 = forms.CharField(label='Confirm new password', widget=forms.PasswordInput)

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not UserBadminton.objects.filter(username=username).exists():
            raise forms.ValidationError("User does not exist.")
        return username

    def clean(self):
        cleaned_data = super().clean()
        new_password1 = cleaned_data.get("new_password1")
        new_password2 = cleaned_data.get("new_password2")

        if new_password1 and new_password2 and new_password1 != new_password2:
            raise forms.ValidationError("The two password fields must match.")