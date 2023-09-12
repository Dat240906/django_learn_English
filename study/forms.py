from django import forms
from .models import ContactModel, WithdrawMoneyModel


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactModel
        fields = '__all__'


class WithdrawMoneyForm(forms.ModelForm):
    class Meta:
        model = WithdrawMoneyModel
        fields = '__all__'



class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class RegisterForm(forms.Form):
    username = forms.CharField(max_length=12)
    password = forms.CharField(max_length=12,widget=forms.PasswordInput)
    confirm_password = forms.CharField(max_length=12,widget=forms.PasswordInput)
