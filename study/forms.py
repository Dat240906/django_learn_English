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


