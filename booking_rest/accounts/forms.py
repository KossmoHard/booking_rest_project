from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError


class RegistrationForm(forms.ModelForm):
    public_name = forms.CharField(min_length=8, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    username = forms.CharField(min_length=4, widget=forms.TextInput(attrs={'class': 'form-control'}))
    phone_number = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    city = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = get_user_model()
        fields = ['public_name', 'username', 'email', 'password', 'phone_number', 'city']


class LoginForm(forms.Form):
    username = forms.CharField(min_length=4, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def clean_username(self):
        username = self.cleaned_data['username']
        if not get_user_model().objects.filter(username=username):
            raise ValidationError('This user does not exist.')
        return username



