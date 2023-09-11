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
    username = forms.CharField(label='Tên đăng nhập')
    password = forms.CharField(label='Mật khẩu', widget=forms.PasswordInput)

class RegisterForm(forms.Form):
    username = forms.CharField(label='Tên đăng nhập')
    password = forms.CharField(label='Mật khẩu', widget=forms.PasswordInput)
    confirm_password = forms.CharField(label='Xác nhận mật khẩu', widget=forms.PasswordInput)
